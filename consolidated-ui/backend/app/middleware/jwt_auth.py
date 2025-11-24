"""
JWT Authentication Middleware
Verifies JWT tokens and attaches user context to requests
"""

from datetime import datetime
from typing import Callable, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token
from app.database import get_db
from app.models.user import User, UserRole

# HTTP Bearer token scheme
security = HTTPBearer()


class AuthenticationError(HTTPException):
    """Custom authentication error"""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    """Custom authorization error"""
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token

    Args:
        credentials: HTTP Authorization header with Bearer token
        db: Database session

    Returns:
        Authenticated User object

    Raises:
        AuthenticationError: If token is invalid or user not found
    """
    token = credentials.credentials

    # Verify token
    payload = verify_token(token, token_type="access")
    if not payload:
        raise AuthenticationError("Invalid or expired token")

    # Extract user_id from token
    user_id: str = payload.get("sub")
    if not user_id:
        raise AuthenticationError("Invalid token payload")

    try:
        user_id_int = int(user_id)
    except (ValueError, TypeError):
        raise AuthenticationError("Invalid user ID in token")

    # Fetch user from database
    result = await db.execute(
        select(User).where(User.id == user_id_int)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise AuthenticationError("User not found")

    if not user.is_active:
        raise AuthenticationError("User account is inactive")

    # Update last_login timestamp
    user.last_login = datetime.utcnow()
    await db.commit()

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current active user

    Args:
        current_user: Current authenticated user

    Returns:
        Active User object

    Raises:
        AuthenticationError: If user is inactive
    """
    if not current_user.is_active:
        raise AuthenticationError("User account is inactive")

    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get current admin user (role-based access control)

    Args:
        current_user: Current authenticated user

    Returns:
        Admin User object

    Raises:
        AuthorizationError: If user is not admin
    """
    if current_user.role != UserRole.ADMIN:
        raise AuthorizationError("Admin privileges required")

    return current_user


def require_role(required_role: UserRole) -> Callable:
    """
    Dependency factory for role-based access control

    Usage:
        @app.get("/admin/users")
        async def get_all_users(user: User = Depends(require_role(UserRole.ADMIN))):
            ...

    Args:
        required_role: Required user role

    Returns:
        Dependency function
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise AuthorizationError(f"Role '{required_role.value}' required")
        return current_user

    return role_checker


# ============ Optional Authentication (for public endpoints with user context) ============

async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to optionally get current user (does not raise error if no token)

    Useful for public endpoints that customize response based on authentication

    Args:
        credentials: Optional HTTP Authorization header
        db: Database session

    Returns:
        User object if authenticated, None otherwise
    """
    if not credentials:
        return None

    try:
        token = credentials.credentials
        payload = verify_token(token, token_type="access")
        if not payload:
            return None

        user_id: str = payload.get("sub")
        if not user_id:
            return None

        user_id_int = int(user_id)

        result = await db.execute(
            select(User).where(User.id == user_id_int, User.is_active == True)
        )
        user = result.scalar_one_or_none()

        return user

    except Exception:
        return None
