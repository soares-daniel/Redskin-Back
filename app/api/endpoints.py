import fastapi

from app.api.dependencies.logging import logging_dependency
from app.api.dependencies.authentication import get_current_user
from app.api.routes import user, event, authentication, role, assets, admin, setup

routers = [user.router, role.router, setup.router, assets.router, admin.router]
main_router = fastapi.APIRouter()

for router in routers:
    main_router.include_router(router, dependencies=[fastapi.Depends(logging_dependency),
                                                     fastapi.Depends(get_current_user)])

# Include authentication router in main router without verifying the user
main_router.include_router(authentication.router, dependencies=[fastapi.Depends(logging_dependency)])

# TODO: FIX THIS, currently workaround
main_router.include_router(event.router, dependencies=[fastapi.Depends(logging_dependency)])
