"""
Services and utility functions for the `standard-timer` operations
"""

from typing import Optional

# TODO: Implement this file to run services for `standard-timer` operations
from fastapi import Header, HTTPException


async def get_user_header_id(x_user_id: Optional[str] = Header(None)) -> str:
    """
    Gets X-User-ID from provided header
    :param x_user_id: user-id
    :return: user-id if not none, else raise HttpException
    """
    if x_user_id is None:
        raise HTTPException(status_code=400, detail="X-User-ID header required")
    return x_user_id
