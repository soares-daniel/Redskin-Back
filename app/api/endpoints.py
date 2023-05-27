from fastapi import APIRouter

from app.api.routes.user import router as user_router

router = APIRouter()

router.include_router(router=user_router)