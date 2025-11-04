import logging.config
import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

import backend.queries as queries
from backend.db import get_db
from backend.logging import LOGGING_CONFIG
from backend.models import User
from backend.schemas import CreateUserIn, CreateUserOut, GetUserOut

# LOGGING
logging.config.dictConfig(LOGGING_CONFIG)

origins: list[str] = [
    "http://localhost:8000", # Development
    "http://localhost:63342", # Development
    # "https://domain.com",
    # "https://www.domain.com",
]
app = FastAPI(root_path="/api")  # /domain/api/ to view api endpoints

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# include routers below


# global endpoints
@app.get(path="/test")
def test_connection() -> JSONResponse:
    return JSONResponse(
        content={
            "status": "You are now connected to the true-timer API",
        },
        status_code=200,
    )


@app.get("/users/{user_uuid}", response_model=GetUserOut)
async def get_user(
    user_uuid: str, db: AsyncSession = Depends(get_db)
) -> JSONResponse | GetUserOut:
    result: int = is_valid_uuid(user_uuid)
    if not result:
        return JSONResponse(content={"message": "Invalid UUID"}, status_code=400)
    user: User | None = await queries.get_user_by_uuid(user_uuid, db)
    if not user:
        return JSONResponse(content={"message": f"User with UUID:{user_uuid} does not exist"}, status_code=400)
    return GetUserOut(**user.__dict__)


@app.post("/users", response_model=CreateUserOut)
async def create_user(
    data: CreateUserIn, db: AsyncSession = Depends(get_db)
) -> JSONResponse | CreateUserOut:
    result: bool = is_valid_timezone(data.timezone)
    if not result:
        return JSONResponse(status_code=400, content={"message": "Invalid timezone"})
    new_user = User(user_id=uuid.uuid4(), timezone=data.timezone)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return CreateUserOut(**new_user.__dict__)


# helper functions
def is_valid_uuid(user_uuid: str) -> bool:
    """
    Tests if the given uuid is a valid uuid
    :param user_uuid:
    :return: bool: True if is valid uuid, false otherwise
    """
    try:
        uuid.UUID(user_uuid, version=4)
        return True
    except ValueError:
        return False


def is_valid_timezone(timezone: str) -> bool:
    try:
        ZoneInfo(timezone)
        return True
    except ZoneInfoNotFoundError:
        return False
