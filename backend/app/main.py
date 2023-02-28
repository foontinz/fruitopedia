from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.api.api_v1.api_v1 import api_router
from app.db.session import SessionLocal


app = FastAPI(title=settings.PROJECT_NAME)

# Initialize db
init_db(SessionLocal())



if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )



app.include_router(api_router, prefix=settings.API_V1_STR)


