"""
Routing file for standard timer package
"""

# TODO: Implement this file to route requests for `standard-timer` operations, all paths will be prefixed with /standard

import uuid

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db import get_db
from backend.models import StandardTimer, User
from backend.queries import get_user_by_uuid
from backend.standard_timer import services
from backend.standard_timer.schemas import (
    CreateStandardTimerIn,
    CreateStandardTimerOut,
    EndStandardTimerOut,
    PauseStandardTimerOut,
    ResumeStandardTimerOut,
    StartStandardTimerOut,
)

router = APIRouter(prefix="/standard", tags=["standard-timer"])


@router.post("", response_model=CreateStandardTimerOut)
async def create_standard_timer(
    data: CreateStandardTimerIn,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(services.get_user_header_id),
) -> JSONResponse | CreateStandardTimerOut:
    # validate UUID
    try:
        valid_id = uuid.UUID(user_id)
    except ValueError:
        return JSONResponse(status_code=400, content={"message": "Invalid UUID"})
    # validate matching user
    user: User | None = await get_user_by_uuid(user_id, db)
    if not user:
        return JSONResponse(status_code=400, content={"message": "User not found"})
    # create timer
    try:
        timer = StandardTimer(user_id=valid_id, minutes=data.minutes, hours=data.hours)
        # save timer and send response
        db.add(timer)
        await db.commit()
        await db.refresh(timer)
        return CreateStandardTimerOut(
            timer_id=str(timer.id), minutes=timer.minutes, hours=timer.hours
        )
    except ValueError as e:
        # value error thrown from @validates function in `db.py`
        return JSONResponse(status_code=400, content={"message": f"{e.args[0]}"})


@router.post("/start/{timer_id}", response_model=StartStandardTimerOut)
async def start_timer(
    timer_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(services.get_user_header_id),
):
    # TODO: Implement this
    pass


@router.post("/pause/{timer_id}", response_model=PauseStandardTimerOut)
async def pause_timer(
    timer_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(services.get_user_header_id),
):
    # TODO: Implement this
    pass


@router.post("/resume/{timer_id}", response_model=ResumeStandardTimerOut)
async def resume_timer(
    timer_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(services.get_user_header_id),
):
    # TODO: Implement this
    pass


@router.post("/end/{timer_id}", response_model=EndStandardTimerOut)
async def end_timer(
    timer_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(services.get_user_header_id),
):
    # TODO: Implement this
    pass
