from app.core.config import settings
from app.schemas.token import TokenPayload

from bcrypt import hashpw
from datetime import datetime, timedelta

import jwt

def create_access_token(
        subject: str, 
        admin: bool = False) -> str:
    expire =  datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = TokenPayload(
        exp=expire,
        sub=subject, 
        admin=admin).dict()
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password, salt):
    return hashed_password.encode('utf-8') == hashpw(password=plain_password.encode('utf-8'), salt=salt.encode('utf-8'))