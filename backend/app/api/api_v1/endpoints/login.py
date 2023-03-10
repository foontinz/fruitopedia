from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import crud, schemas
from app.utils.authorization import UserCredentials_to_UserCreate
from app.api.deps import get_db
from app.core.security import create_access_token


router = APIRouter()

''' POST /login/register
    This endpoint is used to register a new user and return an access token.
'''
@router.post("/register", response_model=schemas.Token)
async def register(
    db: Session = Depends(get_db), 
    user: schemas.UserCreateCredentials = Body(...)):
    
    if crud.user.read_by_email(db, email=user.email) \
        or crud.user.read_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="User is already exist")
    
    user = UserCredentials_to_UserCreate(user)
    user = crud.user.create(db, obj_in=user)
    if not user:
        raise HTTPException(status_code=400, detail="Error while creating user")
    
    access_token = create_access_token(user)
    return schemas.Token(access_token=access_token, token_type="bearer")

''' POST /login/
    This endpoint is used to authenticate a user and return an access token.
'''
@router.post("/", response_model=schemas.Token)
async def login(
    db: Session = Depends(get_db), 
    user: schemas.UserLoginCredentials = Body(...)):
    
    user = crud.user.authenticate(db, obj_in=user)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password") 
    access_token = create_access_token(user)
    return schemas.Token(access_token=access_token, token_type="bearer")
