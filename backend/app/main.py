from fastapi import FastAPI
from app.core.config import settings
from app.db.init_db import init_db
from app.api.api_v1.api_v1 import api_router
from app.api.deps import get_db

app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(api_router, prefix=settings.API_V1_STR)


# Initialize db
if __name__ == "__main__":
    init_db((get_db()))   




