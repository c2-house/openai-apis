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

    MODEL: str = config("MODEL")
    BASE_MESSAGE_PROMPT: list = config("BASE_MESSAGE_PROMPT", cast=Csv())
    BASE_QUIZ_PROMPT: list = config("BASE_QUIZ_PROMPT", cast=Csv())
    NAME_PROMPT: str = config("NAME_PROMPT")
    SUPABASE_URL: str = config("SUPABASE_URL")
    SUPABASE_KEY: str = config("SUPABASE_KEY")
    MAX_REQUEST_COUNT: int = 30

    TIMEZONE_LOCATION: str = "Asia/Seoul"

    @property
    def TIMEZONE(self) -> tzinfo:
        return timezone(self.TIMEZONE_LOCATION)


settings = AppSettings()
