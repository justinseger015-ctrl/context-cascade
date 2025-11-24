"""
User Model - Multi-User Support with Role-Based Access Control
Implements secure password hashing with bcrypt
"""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, PyEnum):
    """User role enumeration for RBAC"""
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """
    User model for authentication and authorization

    Security:
    - Passwords hashed with bcrypt (passlib)
    - Email validation via pydantic
    - Role-based access control (admin/user)
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False,
        server_default=UserRole.USER.value
    )
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))

    # Optional profile fields
    full_name = Column(String(100))
    bio = Column(Text)
    avatar_url = Column(String(500))

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


class RefreshToken(Base):
    """
    Refresh Token model for session management
    Stores refresh tokens with expiration for secure logout/revocation
    """
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # Foreign key to users.id
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    revoked_at = Column(DateTime(timezone=True))

    # Device/session tracking
    user_agent = Column(String(500))
    ip_address = Column(String(45))  # IPv6 compatible

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.revoked})>"
