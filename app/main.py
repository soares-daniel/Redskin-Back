from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.events import shutdown_handler, startup_handler
from app.api.endpoints import router
from app.config.manager import settings


def init_app() -> FastAPI:

    new_app = FastAPI(**settings.attributes)  # type: ignore

    new_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    new_app.add_event_handler("startup", startup_handler(app=new_app))
    new_app.add_event_handler("shutdown", shutdown_handler(app=new_app))

    new_app.include_router(router=router, prefix=settings.API_PREFIX)

    return new_app


app = init_app()


# ===== App Info Endpoints ===== #
@app.get("/")
async def get_health():
    """Get app health"""
    return {"status": "ok"}


@app.get("/info")
async def get_app_info():
    """Get main app info"""
    attributes = settings.attributes
    info = {
        "title": attributes.TITLE,
        "version": attributes.VERSION,
        "debug": attributes.DEBUG,
        "description": attributes.DESCRIPTION,
        "docs_url": attributes.DOCS_URL,
        "openapi_url": attributes.OPENAPI_URL,
        "redoc_url": attributes.REDOC_URL,
        "openapi_prefix": attributes.OPENAPI_PREFIX,
        "api_prefix": attributes.API_PREFIX,
    }

    return info


@app.get("/settings")
async def get_app_settings():
    """Get main env settings"""
    raise NotImplementedError
