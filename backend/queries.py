"""
Global queries used throughout the application
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User


async def get_user_by_uuid(user_uuid: str, db: AsyncSession) -> User | None:
    """
    Gets a user from the database by its UUID
    :param user_uuid: User's UUID
    :param db: Database session
    :return: User or None
    """
    result = await db.scalars(select(User).where(User.user_id == user_uuid))
    return result.one_or_none()
