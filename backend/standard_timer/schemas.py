"""
Schemas for standard-timer processes
"""

from pydantic import BaseModel, Field


class CreateStandardTimerIn(BaseModel):
    minutes: int = Field(
        title="Minutes", description="Minute duration for the timer", ge=0, le=23
    )
    hours: int = Field(
        title="Hours", description="Hour duration for the timer", ge=0, le=24
    )


class CreateStandardTimerOut(BaseModel):
    timer_id: str = Field(title="Timer ID", description="ID for the timer")
    minutes: int = Field(
        title="Minutes",
        description="Maximum allowed minute duration for the timer",
        ge=0,
        le=59,
    )
    hours: int = Field(
        title="Hours",
        description="Maximum allowed hour duration for the timer",
        ge=0,
        le=24,
    )
