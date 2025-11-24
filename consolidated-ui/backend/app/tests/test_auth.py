"""
Authentication Test Suite
Tests user registration, login, JWT tokens, and RBAC
"""

import pytest
from datetime import datetime, timedelta
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, hash_password, verify_password, verify_token
from app.models.user import User, UserRole, RefreshToken


# ============ Unit Tests - Password Hashing ============

def test_password_hashing():
    """Test password hashing and verification"""
    password = "SecurePassword123"
    hashed = hash_password(password)

    # Verify hash is different from original
    assert hashed != password

    # Verify correct password
    assert verify_password(password, hashed) is True

    # Verify incorrect password
    assert verify_password("WrongPassword", hashed) is False


# ============ Unit Tests - JWT Tokens ============

def test_create_access_token():
    """Test JWT access token creation"""
    data = {"sub": "123", "username": "testuser"}
    token = create_access_token(data)

    assert token is not None
    assert isinstance(token, str)

    # Verify token
    payload = verify_token(token, token_type="access")
    assert payload is not None
    assert payload["sub"] == "123"
    assert payload["username"] == "testuser"
    assert payload["type"] == "access"


def test_verify_token_invalid():
    """Test token verification with invalid token"""
    invalid_token = "invalid.token.here"
    payload = verify_token(invalid_token)

    assert payload is None


def test_token_expiration():
    """Test expired token rejection"""
    data = {"sub": "123"}
    # Create token that expired 1 hour ago
    expired_delta = timedelta(hours=-1)
    token = create_access_token(data, expires_delta=expired_delta)

    # Should return None for expired token
    payload = verify_token(token)
    assert payload is None


# ============ Integration Tests - User Registration ============

@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """Test successful user registration"""
    response = await client.post("/api/v1/auth/register", json={
        "username": "testuser1",
        "email": "test1@example.com",
        "password": "SecurePass123",
        "full_name": "Test User"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser1"
    assert data["email"] == "test1@example.com"
    assert data["role"] == "user"
    assert "hashed_password" not in data  # Password should not be returned


@pytest.mark.asyncio
async def test_register_user_weak_password(client: AsyncClient):
    """Test registration with weak password"""
    response = await client.post("/api/v1/auth/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "weak"  # Too short, no uppercase, no digit
    })

    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_duplicate_username(client: AsyncClient, test_user: User):
    """Test registration with duplicate username"""
    response = await client.post("/api/v1/auth/register", json={
        "username": test_user.username,
        "email": "newemail@example.com",
        "password": "SecurePass123"
    })

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, test_user: User):
    """Test registration with duplicate email"""
    response = await client.post("/api/v1/auth/register", json={
        "username": "newusername",
        "email": test_user.email,
        "password": "SecurePass123"
    })

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


# ============ Integration Tests - User Login ============

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user: User):
    """Test successful login"""
    response = await client.post("/api/v1/auth/login", json={
        "username": test_user.username,
        "password": "TestPassword123"  # Default test user password
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["username"] == test_user.username


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """Test login with incorrect password"""
    response = await client.post("/api/v1/auth/login", json={
        "username": test_user.username,
        "password": "WrongPassword123"
    })

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent username"""
    response = await client.post("/api/v1/auth/login", json={
        "username": "nonexistent",
        "password": "AnyPassword123"
    })

    assert response.status_code == 401


# ============ Integration Tests - Protected Endpoints ============

@pytest.mark.asyncio
async def test_get_current_user_success(client: AsyncClient, test_user_token: str):
    """Test accessing protected endpoint with valid token"""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "username" in data
    assert "email" in data


@pytest.mark.asyncio
async def test_get_current_user_no_token(client: AsyncClient):
    """Test accessing protected endpoint without token"""
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 403  # Forbidden


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(client: AsyncClient):
    """Test accessing protected endpoint with invalid token"""
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid.token.here"}
    )

    assert response.status_code == 401


# ============ Integration Tests - Token Refresh ============

@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, test_user: User, db_session: AsyncSession):
    """Test refreshing access token"""
    # Login to get refresh token
    login_response = await client.post("/api/v1/auth/login", json={
        "username": test_user.username,
        "password": "TestPassword123"
    })
    refresh_token = login_response.json()["refresh_token"]

    # Use refresh token to get new access token
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_token_invalid(client: AsyncClient):
    """Test refresh with invalid token"""
    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": "invalid.token"
    })

    assert response.status_code == 401


# ============ Integration Tests - User Logout ============

@pytest.mark.asyncio
async def test_logout_success(client: AsyncClient, test_user: User, test_user_token: str):
    """Test logout revokes refresh token"""
    # Login to get refresh token
    login_response = await client.post("/api/v1/auth/login", json={
        "username": test_user.username,
        "password": "TestPassword123"
    })
    refresh_token = login_response.json()["refresh_token"]

    # Logout
    response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200

    # Try to use revoked refresh token
    refresh_response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })

    assert refresh_response.status_code == 401  # Should be revoked


# ============ Integration Tests - Password Change ============

@pytest.mark.asyncio
async def test_change_password_success(client: AsyncClient, test_user_token: str):
    """Test password change"""
    response = await client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": "TestPassword123",
            "new_password": "NewSecurePass456"
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_password_wrong_current(client: AsyncClient, test_user_token: str):
    """Test password change with wrong current password"""
    response = await client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": "WrongPassword",
            "new_password": "NewSecurePass456"
        },
        headers={"Authorization": f"Bearer {test_user_token}"}
    )

    assert response.status_code == 400


# ============ Integration Tests - Role-Based Access Control ============

@pytest.mark.asyncio
async def test_admin_access(client: AsyncClient, admin_user_token: str):
    """Test admin user can access admin endpoints"""
    # This would test an admin-only endpoint
    # Example: GET /api/v1/admin/users
    pass  # Implement when admin endpoints exist


@pytest.mark.asyncio
async def test_user_cannot_access_admin(client: AsyncClient, test_user_token: str):
    """Test regular user cannot access admin endpoints"""
    # This would test that regular users get 403 on admin endpoints
    pass  # Implement when admin endpoints exist


# ============ Test Fixtures ============

@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create test user"""
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        role=UserRole.USER,
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def admin_user(db_session: AsyncSession) -> User:
    """Create admin test user"""
    user = User(
        username="adminuser",
        email="admin@example.com",
        hashed_password=hash_password("AdminPassword123"),
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def test_user_token(test_user: User) -> str:
    """Create JWT token for test user"""
    return create_access_token({
        "sub": str(test_user.id),
        "username": test_user.username,
        "role": test_user.role.value
    })


@pytest.fixture
def admin_user_token(admin_user: User) -> str:
    """Create JWT token for admin user"""
    return create_access_token({
        "sub": str(admin_user.id),
        "username": admin_user.username,
        "role": admin_user.role.value
    })
