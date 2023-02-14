from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.authorization import salt_hash_user_password
from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token


router = APIRouter()


''' POST /login/access-token
    This endpoint is used to authenticate a user and return an access token.
'''
@router.post("/access-token", response_model=schemas.Token)
async def access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()):
    
    user = crud.user.authenticate(db, form_data)
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
    user: schemas.UserCreateCredentials = Body(...)):
    
    if crud.user.read_by_identifier(db, obj_in=schemas.UserRead(**user.dict(exclude_none=True))):
        raise HTTPException(status_code=400, detail="Email or Username already registered")
    
    user = salt_hash_user_password(user)
    user = crud.user.create(db, obj_in=schemas.UserCreate(**user.dict(exclude_none=True)))
    access_token = create_access_token(user)
    return schemas.Token(access_token=access_token, token_type="bearer")
