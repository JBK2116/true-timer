"""
Schemas for standard-timer processes
"""
from pydantic import BaseModel, Field

from pydantic import BaseModel

class CreateStandardTimer:
    minutes: int = Field(title="Minutes", description="Minute duration for the timer", ge=1, le=23)
    hours: int = Field(title="Hours", description="Hour duration for the timer", ge=1, le=24)


