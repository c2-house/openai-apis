import asyncio
import openai
from typing import Annotated, AsyncIterable
from fastapi import Depends, HTTPException, status
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import AsyncIteratorCallbackHandler
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.schema.exceptions import LangChainException
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


async def get_message_from_openai(
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


async def get_streaming_message_from_opeanai(
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
            stream=True,
        )
        async for token in response:
            try:
                yield token.choices[0]["message"]["content"]
            except KeyError:
                ...
    except openai.InvalidRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    # return content


async def get_streaming_message_with_langchain(
    data: Annotated[MessageRequest, Depends(convert_manner)]
) -> AsyncIterable[str]:
    callback = AsyncIteratorCallbackHandler()
    model = ChatOpenAI(
        model=settings.MODEL,
        temperature=1,
        max_tokens=1024,
        openai_api_key=settings.OPEN_AI_KEY,
    )
    task = asyncio.create_task(
        model.agenerate(
            messages=[
                [
                    SystemMessage(content=MessageBotPrompt._get_system()["content"]),
                    HumanMessage(
                        content=MessageBotPrompt._get_user(
                            settings.BASE_MESSAGE_PROMPT, data
                        )["content"]
                    ),
                    AIMessage(
                        content=MessageBotPrompt._get_assistant(
                            settings.BASE_MESSAGE_PROMPT
                        )["content"]
                    ),
                ]
            ]
        )
    )

    try:
        async for token in callback.aiter():
            yield token
    except LangChainException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    finally:
        callback.done.set()

    await task


HelloMessagePrompt = Annotated[dict, Depends(get_message_from_openai)]
HelloMessageStreamingPrompt = Annotated[
    str, Depends(get_streaming_message_from_opeanai)
]
HelloMessageLangchainStreamingPrompt = Annotated[
    AsyncIterable[str], Depends(get_streaming_message_with_langchain)
]
