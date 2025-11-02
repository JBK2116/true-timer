import logging.config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.logging import LOGGING_CONFIG

# LOGGING
logging.config.dictConfig(LOGGING_CONFIG)

origins: list[str] = [
    "http://localhost:8000",
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


@app.get(path="/test")
def test_connection() -> JSONResponse:
    return JSONResponse(
        content={
            "status": "You are now connected to the true-timer API",
        },
        status_code=200,
    )
