from app.core.config import settings
from app.schemas.token import TokenPayload
from app.models.user import User

from bcrypt import hashpw
from datetime import datetime, timedelta

import jwt

def create_access_token(user:User) -> str:
    expire =  datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = TokenPayload(
        exp=expire,
        sub=user.id, 
        admin=user.is_superuser).dict()
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password, salt):
    return hashed_password.encode('utf-8') == hashpw(password=plain_password.encode('utf-8'), salt=salt.encode('utf-8'))