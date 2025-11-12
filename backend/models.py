"""
All models for this web application will go here
"""

from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

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
    # track start and end time
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,  # set when user explicitly starts timer
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    # track state
    elapsed_seconds: Mapped[int] = mapped_column(
        default=0
    )  # tracks cumulative elapsed seconds
    total_paused_seconds: Mapped[int] = mapped_column(
        default=0
    )  # tracks cumulative total paused seconds
    total_pause_count: Mapped[int] = mapped_column(
        default=0
    )  # tracks total pause count
    last_pause_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )  # updated on every pause request
    is_started: Mapped[bool] = mapped_column(default=False)  # set on start request
    is_paused: Mapped[bool] = mapped_column(
        default=False
    )  # updated on every pause/resume request
    is_completed: Mapped[bool] = mapped_column(default=False)  # updated on end request


class User(TimeStampMixin, Base):
    # One User to Many Timers
    __tablename__ = "users"
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    timezone: Mapped[str] = mapped_column(nullable=False)
    standard_timers: Mapped[list["StandardTimer"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class StandardTimer(TimerMixin, TimeStampMixin, Base):
    # Many StandardTimers to One User
    __tablename__ = "standard_timer"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.user_id"))
    user: Mapped["User"] = relationship()
    minutes: Mapped[int] = mapped_column(nullable=False)
    hours: Mapped[int] = mapped_column(nullable=False)

    @validates("minutes", "hours")
    def validate_duration(self, key, value) -> int:
        """
        Validates duration value fields (minutes and hours)
        :param key: current field being evaluated
        :param value: value of current field being evaluated
        """
        if key == "minutes" and (value < 0 or value > 59):
            raise ValueError("Minutes must be between 1 and 59 inclusive")
        if key == "hours" and (value < 0 or value > 23):
            raise ValueError("Hours must be between 0 and 23 inclusive")
        minutes = value if key == "minutes" else getattr(self, "minutes", 0)
        hours = value if key == "hours" else getattr(self, "hours", 0)
        if minutes == 0 and hours == 0:
            raise ValueError("Timer duration must be at least 1 minute")
        return value
