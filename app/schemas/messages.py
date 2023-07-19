from pydantic import BaseModel, validator


class MessageResponse(BaseModel):
    results: list

    @validator("results")
    def check_results(cls, v):
        if len(v) != 3:
            raise ValueError("Results must be 3")
        return v
