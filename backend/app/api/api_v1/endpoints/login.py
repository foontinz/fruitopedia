from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCredentials
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app import crud, schemas

from bcrypt import hashpw

router = APIRouter()


''' POST /login/access-token
    This endpoint is used to authenticate a user and return an access token.
'''
@router.post("/access-token", response_model=schemas.Token)
async def access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = crud.user.authenticate(db, UserCredentials(email=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(subject=user.email, admin=user.is_superuser)
    return schemas.Token(access_token=access_token, token_type="bearer")

''' POST /login/register
    This endpoint is used to register a new user and return an access token.
'''
@router.post("/register", response_model=schemas.Token)
async def register(
    db: Session = Depends(get_db), 
    user: schemas.UserCreate = Body(...)):
    
    user.hashed_password = hashpw(password=user.password.encode('utf-8'), salt=user.salt.encode('utf-8')).decode('utf-8')
    user.password = None
    user = crud.user.create(db, obj_in=user)
    access_token = create_access_token(subject=user.email, admin=user.is_superuser)
    return schemas.Token(access_token=access_token, token_type="bearer")
