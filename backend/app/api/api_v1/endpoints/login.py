from fastapi import APIRouter
from app import schemas


router = APIRouter()

@router.post("/", response_model=schemas.User)
def login_user():