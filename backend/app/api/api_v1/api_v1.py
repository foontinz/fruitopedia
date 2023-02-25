from fastapi import APIRouter

from app.api.api_v1.endpoints import login
from app.api.api_v1.endpoints import fruit

api_router = APIRouter()
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(fruit.router, prefix="/fruit", tags=["fruit"])
# api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
