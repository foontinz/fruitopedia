from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.init_db import init_db
from app.api.api_v1.api_v1 import api_router
from app.db.session import SessionLocal


app = FastAPI(title=settings.PROJECT_NAME)

# Initialize db
init_db(SessionLocal())


app.include_router(api_router, prefix=settings.API_V1_STR)


