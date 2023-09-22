import openai
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.dependencies.requests import check_secret_header
from app.core.prompts.quizzes import QuizPrompt
from app.schemas.quizzes import QuizResponse
from app.core.config import settings

router = APIRouter()


@router.get(
    "/", dependencies=[Depends(check_secret_header)], response_model=QuizResponse
)
async def get_generated_quiz(artist: str):
    """
    Send request to OPEN AI
    Generate quiz
    """

    try:
        response = await openai.ChatCompletion.acreate(
            model=settings.MODEL,
            messages=QuizPrompt.make_prompt(artist),
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        content = response.choices[0]["message"]["content"]
    except openai.InvalidRequestError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {"results": content}
