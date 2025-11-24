"""
User Pydantic Schemas - Request/Response validation
Implements strong validation for email and password security
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.user import UserRole


# ============ Request Schemas ============

class UserRegister(BaseModel):
    """User registration request schema"""
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: Optional[str] = Field(None, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """
        Validate password strength (OWASP recommendations):
        - Minimum 8 characters
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 digit
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least 1 uppercase letter")

        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least 1 lowercase letter")

        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least 1 digit")

        return v


class UserLogin(BaseModel):
    """User login request schema"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class UserUpdate(BaseModel):
    """User profile update schema"""
    full_name: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = Field(None, max_length=500)


class PasswordChange(BaseModel):
    """Password change request schema"""
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)

    @field_validator("new_password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Same password validation as registration"""
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least 1 uppercase letter")

        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least 1 lowercase letter")

        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least 1 digit")

        return v


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str = Field(..., min_length=1)


# ============ Response Schemas ============

class UserResponse(BaseModel):
    """User response schema (excludes sensitive data)"""
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    full_name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """JWT token response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class TokenVerifyResponse(BaseModel):
    """Token verification response"""
    valid: bool
    user_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[UserRole] = None


class LoginResponse(BaseModel):
    """Login response with user data and tokens"""
    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    detail: Optional[str] = None
