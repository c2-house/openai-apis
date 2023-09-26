from datetime import datetime
from fastapi import Request, HTTPException, status
from supabase import Client
from app.core.config import settings


def _get_ip(request: Request) -> str:
    ip = (
        request.headers["x-forwarded-for"]
        if "x-forwarded-for" in request.headers.keys()
        else request.client.host
    )
    return ip.split(",")[0] if "," in ip else ip


def check_usage_restriction(request: Request, ip: str, supabase: Client):
    supabase = request.state.supabase
    response = (
        supabase.table("usage_restriction")
        .select("*")
        .eq("identifier", ip)
        .order("created_at", desc=True)
        .execute()
    )

    if len(response.data) > 0:
        time = response.data[0].get("created_at")
        time = datetime.fromisoformat(time)
        today = datetime.now(settings.TIMEZONE).date()
        if time.date() == today:
            count = response.data[0].get("count")
            if count >= settings.MAX_REQUEST_COUNT:
                return HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="오늘 사용량을 모두 사용하셨습니다. 내일 다시 이용해주세요.",
                )
            else:
                return response, "update"
        elif time.date() <= today:
            return response, "create"
    else:
        return response, "create"


def update_count(request: Request):
    ip = _get_ip(request)
    supabase = request.state.supabase
    response, type = check_usage_restriction(request, ip, supabase)
    if type == "create":
        supabase.table("usage_restriction").insert(
            {
                "identifier": ip,
                "count": 1,
                "created_at": datetime.now(settings.TIMEZONE).isoformat(),
            }
        ).execute()
    elif type == "update":
        count = response.data[0].get("count")
        id = response.data[0].get("id")
        supabase.table("usage_restriction").update({"count": count + 1}).eq(
            "id", id
        ).execute()
