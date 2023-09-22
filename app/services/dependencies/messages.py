import openai
from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.core.prompts.messages import MessageBotPrompt
from app.core.config import settings
from app.schemas.messages import MessageRequest


async def convert_manner(data: MessageRequest) -> MessageRequest:
    """
    Convert manner
    """
    if data.manner == "반말":
        data.manner = "without honorifics"
    elif data.manner == "존댓말":
        data.manner = "with honorifics"
    return data


async def send_prompt_to_openai(
    data: Annotated[MessageRequest, Depends(convert_manner)]
) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.MODEL,
            messages=MessageBotPrompt.make_prompt(data),
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


HelloMessagePrompt = Annotated[dict, Depends(send_prompt_to_openai)]
