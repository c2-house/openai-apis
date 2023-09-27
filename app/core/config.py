from pathlib import Path
from pytz import timezone, tzinfo
from pydantic_settings import BaseSettings
from decouple import AutoConfig, Csv

BASE_DIR = Path(__file__).resolve().parent.parent
config = AutoConfig(search_path=BASE_DIR)


class AppSettings(BaseSettings):
    DEBUG: bool = config("DEBUG", default=True, cast=bool)
    OPEN_AI_KEY: str = config("OPEN_AI_KEY")
    SECRET: str = config("SECRET", default="dev")
    DOCS_URL: str = config("DOCS_URL", default="/api/docs")
    REDOC_URL: str = config("REDOC_URL", default="/api/redoc")
    HEALTH_CHECK_PATH: str = "/health-check/"

    MODEL: str = config("MODEL")
    BASE_MESSAGE_PROMPT: list = config("BASE_MESSAGE_PROMPT", cast=Csv())
    BASE_QUIZ_PROMPT: list = config("BASE_QUIZ_PROMPT", cast=Csv())
    NAME_PROMPT: str = config("NAME_PROMPT")
    SUPABASE_URL: str = config("SUPABASE_URL")
    SUPABASE_KEY: str = config("SUPABASE_KEY")
    MAX_REQUEST_COUNT: int = 30

    TIMEZONE_LOCATION: str = "Asia/Seoul"

    LOG_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "requests": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    @property
    def TIMEZONE(self) -> tzinfo:
        return timezone(self.TIMEZONE_LOCATION)


settings = AppSettings()
