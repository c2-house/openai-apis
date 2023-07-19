from typing import Annotated
from fastapi import Header, HTTPException, status
from app.core.config import settings


async def check_secret_header(secret: Annotated[str, Header()] = None):
    """
    Check secret header
    Authorized personnel only
    """
    if secret != settings.SECRET:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid secret header"
        )
