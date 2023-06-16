from fastapi import APIRouter

from app.api.routes.user import router as user_router
from app.api.routes.event import router as event_router

router = APIRouter()

router.include_router(router=user_router)
router.include_router(router=event_router)
