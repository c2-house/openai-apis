from fastapi import APIRouter, Depends, status
from app.services.dependencies.messages import HelloMessagePrompt
from app.services.dependencies.requests import check_secret_header
from app.schemas.messages import MessageResponse


router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(check_secret_header)],  # FIXME: 추후 변경
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="OPEN AI에 프롬프트 전달하기",
)
async def get_generated_messages(results: HelloMessagePrompt):
    """
    ## OPEN AI에 프롬프트 전달하기
    - name: str (Optional)
    - relation: str
    - reason: str
    - manner: str
    - max_length: str
    """
    return results
