from fastapi import APIRouter
from app.api.auth.api import router as auth_router
from app.api.users.api import router as user_router
from app.api.applications.api import router as app_router
from app.api.types.api import router as type_router
from app.api.files.api import router as file_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (auth_router, "auth", "Security"),
    (user_router, "users", "Users"),
    (app_router, "apps", "Apps"),
    (type_router, "types", "Types"),
    (file_router, "files", "Files")
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
