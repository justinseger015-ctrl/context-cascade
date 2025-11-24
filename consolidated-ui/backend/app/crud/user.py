"""
User CRUD Operations
Implements secure user management with role-based access control
"""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User, UserRole


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Get user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get user by username"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get user by email"""
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()


async def get_all_users(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    include_inactive: bool = False
) -> list[User]:
    """
    Get all users (admin only)

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        include_inactive: Include inactive users

    Returns:
        List of User objects
    """
    query = select(User)

    if not include_inactive:
        query = query.where(User.is_active == True)

    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def create_user(
    db: AsyncSession,
    username: str,
    email: str,
    password: str,
    role: UserRole = UserRole.USER,
    **kwargs
) -> User:
    """
    Create new user

    Args:
        db: Database session
        username: Unique username
        email: Unique email
        password: Plain text password (will be hashed)
        role: User role (default: USER)
        **kwargs: Additional user fields (full_name, bio, etc.)

    Returns:
        Created User object
    """
    hashed_pwd = hash_password(password)

    user = User(
        username=username,
        email=email,
        hashed_password=hashed_pwd,
        role=role,
        is_active=True,
        is_verified=False,
        **kwargs
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def update_user(
    db: AsyncSession,
    user_id: int,
    **kwargs
) -> Optional[User]:
    """
    Update user fields

    Args:
        db: Database session
        user_id: User ID to update
        **kwargs: Fields to update

    Returns:
        Updated User object or None if not found
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        return None

    # Update allowed fields
    for key, value in kwargs.items():
        if hasattr(user, key) and key != "hashed_password":
            setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """
    Soft delete user (set is_active=False)

    Args:
        db: Database session
        user_id: User ID to delete

    Returns:
        True if deleted, False if not found
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        return False

    user.is_active = False
    await db.commit()

    return True


async def change_user_password(
    db: AsyncSession,
    user_id: int,
    old_password: str,
    new_password: str
) -> bool:
    """
    Change user password with verification

    Args:
        db: Database session
        user_id: User ID
        old_password: Current password for verification
        new_password: New password to set

    Returns:
        True if password changed, False if verification failed
    """
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        return False

    # Verify old password
    if not verify_password(old_password, user.hashed_password):
        return False

    # Set new password
    user.hashed_password = hash_password(new_password)
    await db.commit()

    return True
