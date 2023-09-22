from pydantic import BaseModel, validator


class MessageRequest(BaseModel):
    name: str | None = None
    relation: str
    reason: str
    manner: str
    max_length: str


class MessageResponse(BaseModel):
    results: list

    @validator("results")
    def check_results(cls, v):
        if len(v) != 3:
            raise ValueError("Results must be 3")
        return v
