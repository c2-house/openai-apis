from fastapi import APIRouter
from app.routes.apis.messages import router as messages_router
from app.routes.apis.quizzes import router as quizzes_router


router = APIRouter()
router.include_router(messages_router, prefix="/messages", tags=["messages"])
router.include_router(quizzes_router, prefix="/quizzes", tags=["quizzes"])
