from pydantic import BaseModel


class QuizResponse(BaseModel):
    results: str
