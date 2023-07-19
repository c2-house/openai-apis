import openai
from fastapi import FastAPI
from app.core.config import settings
from app.routes.routers import router as api_router

openai.api_key = settings.OPEN_AI_KEY

app = FastAPI(docs_url=settings.DOCS_URL, redoc_url=settings.REDOC_URL)

app.include_router(api_router)
