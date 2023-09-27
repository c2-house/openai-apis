import openai
from typing import Annotated
from fastapi import Depends, HTTPException, Request, status
from app.schemas.messages import MessageRequest
from app.services.supabase.messages import update_count
from app.core.prompts.messages import MessageBotPrompt
from app.core.config import settings


async def convert_manner(data: MessageRequest) -> MessageRequest:
    """
    Convert manner
    """
    if data.manner == "반말":
        data.manner = "without honorifics, use Korean informal language"
    elif data.manner == "존댓말":
        data.manner = "with honorifics"
    return data


async def get_message_from_openai(
    request: Request, data: Annotated[MessageRequest, Depends(convert_manner)]
) -> dict:
    update_count(request)
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


async def get_streaming_message_from_openai(data: MessageRequest) -> dict:
    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.MODEL,
            messages=MessageBotPrompt.make_prompt(data),
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stream=True,
        )
        async for chunk in response:
            try:
                yield chunk["choices"][0]["delta"].get("content", "")
            except KeyError:
                pass
    except openai.InvalidRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


HelloMessagePrompt = Annotated[dict, Depends(get_message_from_openai)]
HelloMessageStreamingPrompt = Annotated[str, Depends(get_streaming_message_from_openai)]
