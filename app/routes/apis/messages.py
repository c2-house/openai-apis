import openai
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies.messages import MessageQueryParams, convert_manner_params
from app.core.dependencies.requests import check_secret_header
from app.core.prompts.messages import MessageBotPrompt
from app.schemas.messages import MessageResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/", dependencies=[Depends(check_secret_header)], response_model=MessageResponse
)
async def get_generated_messages(
    query_params: Annotated[MessageQueryParams, Depends(convert_manner_params)]
):
    """
    Send request to OPEN AI
    Generate messages for user to choose one of them
    """

    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.MODEL,
            messages=MessageBotPrompt.make_prompt(query_params),
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        content = response.choices[0]["message"]["content"]
        content = content.split("\n")
        results = [sentence.strip() for sentence in content if sentence.strip()]
    except openai.InvalidRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"results": results}
