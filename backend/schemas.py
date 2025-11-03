"""
Global Pydantic schemas used throughout the application
"""

import uuid
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateUserIn(BaseModel):
    timezone: str = Field(
        min_length=3,
        max_length=35,
        description="The timezone associated with the user's browser",
        example="America/New_York",
        title="IANA Timezone",
        strict=True,
    )


class CreateUserOut(BaseModel):
    user_id: UUID = Field(
        title="UUID",
        description="The created user ID in UUID4 format",
        example=uuid.uuid4(),
    )
    timezone: str = Field(
        title="IANA Timezone",
        example="America/New_York",
        strict=True,
        description="The timezone associated with the user's browser",
    )
    model_config = ConfigDict(from_attributes=True)


class GetUserOut(BaseModel):
    user_id: UUID = Field(
        title="UUID", description="The user's ID in UUID4 format", example=uuid.uuid4()
    )
    timezone: str = Field(
        title="IANA Timezone",
        example="America/New_York",
        strict=True,
        description="The timezone associated with the user's browser",
    )
    model_config = ConfigDict(from_attributes=True)
