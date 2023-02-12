from fastapi import FastAPI, Query
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title=settings.PROJECT_NAME)



# add middleware for cors

app.include_router(api_router, prefix=settings.API_V1_STR)


