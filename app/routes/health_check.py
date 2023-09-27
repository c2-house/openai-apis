from fastapi import APIRouter, status


router = APIRouter()


@router.get("/health-check/", status_code=status.HTTP_200_OK, response_model=dict)
async def health_check():
    """
    Health check
    """
    return {"status": "ok"}
