from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from app.services.dependencies.messages import (
    HelloMessagePrompt,
    HelloMessageStreamingPrompt,
)
from app.services.dependencies.requests import check_secret_header
from app.schemas.messages import MessageResponse


router = APIRouter()


@router.post(
    "/",
    dependencies=[Depends(check_secret_header)],  # FIXME: 추후 변경
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="인사말 생성하기",
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


@router.post(
    "/streaming",
    dependencies=[Depends(check_secret_header)],  # FIXME: 추후 변경
    response_model=str,
    status_code=status.HTTP_200_OK,
    summary="인사마 생성하기 (스트리밍)",
)
async def get_generated_messages_streaming(results: HelloMessageStreamingPrompt):
    """
    ## OPEN AI에 프롬프트 전달하기
    - name: str (Optional)
    - relation: str
    - reason: str
    - manner: str
    - max_length: str
    """
    return StreamingResponse(results, media_type="text/event-stream")
