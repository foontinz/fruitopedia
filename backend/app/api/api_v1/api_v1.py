from fastapi import APIRouter

from app.api.api_v1.endpoints import login, fruit, variety, country





api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(fruit.router, prefix="/fruit", tags=["fruit"])
api_router.include_router(variety.router, prefix="/variety", tags=["variety"])
api_router.include_router(country.router, prefix="/country", tags=["country"])
