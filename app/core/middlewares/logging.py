import json
import time
import logging
from logging.config import dictConfig
from datetime import datetime
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import StreamingResponse
from starlette.concurrency import iterate_in_threadpool
from app.core.config import settings


LOGGER = logging.getLogger("requests")


class LoggingMixin:
    async def get_log_dict(
        self,
        request: Request,
        response: StreamingResponse | None,
        status_code: int,
        error=None,
    ) -> dict:
        log_dict = {
            "URL": request.url.hostname + request.url.path,
            "Method": request.method,
            "Status-Code": status_code,
            "IP": self.get_ip(request),
            "Error-Message": await self.get_err_msg(response, error),
            "User-Agent": request.headers.get("user-agent", None),
            "Process-Time": str(
                round((time.time() - request.state.start_time) * 1000, 5)
            )
            + "ms",
            "Request-Time": datetime.now(settings.TIMEZONE).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
        return log_dict

    def get_ip(self, request: Request) -> str:
        ip = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else request.client.host
        )
        return ip.split(",")[0] if "," in ip else ip

    async def get_err_msg(self, response: StreamingResponse | None, error=None) -> str:
        if error:
            err_msg = error.detail
        else:
            if response.status_code >= 400:
                response_body = [section async for section in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
                err_msg = response_body[0].decode("utf-8")
                err_msg = json.loads(err_msg)["detail"]
            else:
                return None
        return err_msg

    def get_status_code(self, response, error=None) -> int:
        try:
            if error:
                status_code = error.status_code
            else:
                status_code = response.status_code
        except AttributeError:
            error.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            status_code = error.status_code
        finally:
            return status_code

    def is_pre_flight(self, request: Request):
        method = str(request.method)
        if method == "OPTIONS":
            return True
        return False

    def check_request_header(self, request: Request):
        check = request.headers.get("Authorization", None)
        return check

    def check_allowed_hosts(self, request: Request, allowed_hosts: list[str]) -> bool:
        if request.url.hostname in allowed_hosts:
            return True
        return False


async def exception_handler(error: Exception) -> HTTPException:
    if not isinstance(error, HTTPException):
        error = HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )
    return error


class LoggingMiddleware(BaseHTTPMiddleware, LoggingMixin):
    def __init__(self, app, logger):
        self.logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        if (
            self.is_pre_flight(request)
            or request.url.path == settings.HEALTH_CHECK_PATH
            or not self.check_allowed_hosts(request, settings.ALLOWED_HOSTS)
        ):
            response = await call_next(request)
            return response

        try:
            request.state.start_time = time.time()
            response = await call_next(request)
            status_code = self.get_status_code(response)
            log_dict = await self.get_log_dict(request, response, status_code)
        except Exception as e:
            e = await exception_handler(e)
            status_code = self.get_status_code(None, e)
            log_dict = await self.get_log_dict(request, None, status_code, e)
            log_str = ", ".join(f"{key}: {value}" for key, value in log_dict.items())
            self.logger.error(log_str)
            return await call_next(request)
        else:
            log_str = ", ".join(f"{key}: {value}" for key, value in log_dict.items())
            self.logger.info(log_str)
            return response


dictConfig(settings.LOG_CONFIG)
