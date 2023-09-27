import openai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.middlewares.logging import LoggingMiddleware, LOGGER
from app.routes.routers import router as api_router
from app.routes.health_check import router as health_check_router

openai.api_key = settings.OPEN_AI_KEY

app = FastAPI(
    docs_url=settings.DOCS_URL, redoc_url=settings.REDOC_URL, lifespan=lifespan
)

app.include_router(api_router)
app.include_router(health_check_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:3000", "172.30.1.27:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware, logger=LOGGER)
