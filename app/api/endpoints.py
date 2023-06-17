import fastapi

from app.api.routes import user, event, authentication

routers = [user.router, event.router, authentication.router]
main_router = fastapi.APIRouter()

for router in routers:
    main_router.include_router(router)
