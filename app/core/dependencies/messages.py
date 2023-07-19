from typing import Annotated
from fastapi import Depends


class MessageQueryParams:
    """
    Message Query Params
    who: 누구
    relation: 어떤 관계
    reason: 무슨 이유로
    manner: 반말 or 존댓말
    max_length: 메세지 최대 길이
    """

    def __init__(
        self,
        *,
        who: str | None = None,
        relation: str,
        reason: str,
        manner: str,
        max_length: str
    ):
        self.who = who
        self.relation = relation
        self.reason = reason
        self.manner = manner
        self.max_length = max_length


async def convert_manner_params(
    query_params: Annotated[MessageQueryParams, Depends(MessageQueryParams)]
):
    """
    Convert manner
    """
    if query_params.manner == "반말":
        query_params.manner = "without honorifics"
    elif query_params.manner == "존댓말":
        query_params.manner = "with honorifics"
    return query_params
