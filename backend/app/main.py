from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api_v1.api_v1 import api_router


app = FastAPI(title=settings.PROJECT_NAME)




app.include_router(api_router, prefix=settings.API_V1_STR)


