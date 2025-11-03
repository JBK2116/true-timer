"""
All models for this web application will go here
"""

from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.db import Base


class TimeStampMixin:
    # Database uses stores time in UTC by default
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class TimerMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    pause_count: Mapped[int] = mapped_column(default=0)


class User(TimeStampMixin, Base):
    # One User to Many Timers
    __tablename__ = "users"
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    timezone: Mapped[str] = mapped_column(nullable=False)


class StandardTimer(TimerMixin, Base):
    # Many StandardTimers to One User
    __tablename__ = "standard_timer"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship()
