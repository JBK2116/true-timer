"""
Schemas for standard-timer processes
"""

from pydantic import BaseModel, Field


class CreateStandardTimerIn(BaseModel):
    minutes: int = Field(
        title="Minutes", description="Minute duration for the timer", ge=0, le=59
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


class StartStandardTimerOut(BaseModel):
    # timer identification
    timer_id: str = Field(title="Timer ID", description="ID for the timer")
    # timer duration
    minutes: int = Field(
        title="Minutes", description="Minute duration for the timer", ge=0, le=59
    )
    hours: int = Field(
        title="Hours", description="Hour duration for the timer", ge=0, le=24
    )
    # timer state
    elapsed_seconds: int = Field(
        title="Elapsed seconds", description="Elapsed seconds for the timer", ge=0
    )
    total_paused_seconds: int = Field(
        title="Total paused seconds",
        description="Total paused seconds for the timer",
        ge=0,
    )
    is_paused: bool = Field(
        title="Is paused", description="Whether the timer is currently paused"
    )
    total_pause_count: int = Field(
        title="Pause count", description="Pause count for the timer", ge=0
    )
    # timer timestamps
    start_time: str = Field(
        title="Start time ISO", description="Start time in ISO 8601 format"
    )
    last_pause_time: str | None = Field(
        title="Last pause time ISO",
        description="Last pause time in ISO 8601 format, null if not paused",
    )
    # formatted display strings
    start_time_string: str = Field(
        title="Start time display", description="Formatted start time for display"
    )
    end_time_string: str = Field(
        title="End time display", description="Formatted end time for display"
    )


class PauseStandardTimerOut(BaseModel):
    # timer identification
    timer_id: str = Field(title="Timer ID", description="ID for the timer")
    # pause state
    last_pause_time: str | None = Field(
        title="Last pause time ISO",
        description="Last pause time in ISO 8601 format, null if not paused",
    )
    total_pause_count: int = Field(
        title="Pause count", description="Pause count for the timer", ge=0
    )
    is_paused: bool = Field(
        title="Is paused", description="Whether the timer is currently paused"
    )


class ResumeStandardTimerOut(BaseModel):
    # timer identification
    timer_id: str = Field(title="Timer ID", description="ID for the timer")
    # pause state
    total_paused_seconds: int = Field(
        title="Total paused seconds",
        description="Total paused seconds for the timer",
        ge=0,
    )


class EndStandardTimerOut(BaseModel):
    # timer identification
    timer_id: str = Field(title="Timer ID", description="ID for the timer")
    # timer statistics
    end_time_string: str = Field(
        title="End time display", description="Formatted end time for display"
    )
    total_pause_count: int = Field(
        title="Pause count", description="Pause count for the timer", ge=0
    )
