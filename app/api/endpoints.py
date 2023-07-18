import fastapi

from app.api.dependencies.logging import logging_dependency
from app.api.routes import user, event, authentication, role, admin

routers = [user.router, event.router, authentication.router, role.router, admin.router]
main_router = fastapi.APIRouter()

# Global logging dependency, can be used in any router or endpoint individually
for router in routers:
    main_router.include_router(router, dependencies=[fastapi.Depends(logging_dependency)])
