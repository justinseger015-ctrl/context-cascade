"""
JWT Authentication and Authorization Middleware
OWASP API1:2023 - Broken Object Level Authorization (BOLA) mitigation
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.config.settings import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# HTTP Bearer token scheme
security = HTTPBearer()


class TokenData(BaseModel):
    """JWT token payload data"""
    user_id: int
    email: str
    exp: datetime


class User(BaseModel):
    """Current authenticated user"""
    id: int
    email: str


def create_access_token(user_id: int, email: str) -> str:
    """
    Create JWT access token

    Args:
        user_id: User ID
        email: User email

    Returns:
        Encoded JWT token
    """
    expires_delta = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    expire = datetime.utcnow() + expires_delta

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def create_refresh_token(user_id: int, email: str) -> str:
    """
    Create JWT refresh token

    Args:
        user_id: User ID
        email: User email

    Returns:
        Encoded JWT refresh token
    """
    expires_delta = timedelta(days=settings.JWT_REFRESH_EXPIRATION_DAYS)
    expire = datetime.utcnow() + expires_delta

    payload = {
        "user_id": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


def verify_jwt_token(token: str) -> TokenData:
    """
    Verify and decode JWT token

    Args:
        token: JWT token string

    Returns:
        TokenData with user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )

        user_id: int = payload.get("user_id")
        email: str = payload.get("email")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"))

        if user_id is None or email is None:
            logger.warning(f"Invalid token payload: missing user_id or email")
            raise credentials_exception

        return TokenData(user_id=user_id, email=email, exp=exp)

    except JWTError as e:
        logger.warning(f"JWT validation error: {e}")
        raise credentials_exception


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    FastAPI dependency to get current authenticated user

    Usage:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id, "email": user.email}

    Args:
        credentials: HTTP Bearer token from request header

    Returns:
        User object with current user information

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    token_data = verify_jwt_token(token)

    return User(id=token_data.user_id, email=token_data.email)


def verify_resource_ownership(user_id: int, resource_user_id: int) -> None:
    """
    OWASP API1:2023 - Broken Object Level Authorization (BOLA) mitigation
    Verify that the current user owns the requested resource

    Args:
        user_id: Current authenticated user ID
        resource_user_id: User ID associated with the resource

    Raises:
        HTTPException: 403 Forbidden if user doesn't own the resource
    """
    if user_id != resource_user_id:
        logger.warning(
            f"Authorization failed: user {user_id} attempted to access "
            f"resource owned by user {resource_user_id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource"
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[User]:
    """
    FastAPI dependency to get current user if authenticated, None otherwise
    Useful for endpoints that work with or without authentication

    Args:
        credentials: Optional HTTP Bearer token

    Returns:
        User object if authenticated, None otherwise
    """
    if credentials is None:
        return None

    try:
        token_data = verify_jwt_token(credentials.credentials)
        return User(id=token_data.user_id, email=token_data.email)
    except HTTPException:
        return None
