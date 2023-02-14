from pydantic import BaseModel, EmailStr, validator
from typing import Any
import re
from bcrypt import hashpw, gensalt

class UserBase(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    username: str | None = None
    fullname: str | None = None
    hashed_password: str | None = None
    salt: str | None = None   
    is_banned: bool = False
    is_superuser: bool = False

    class Config:
        orm_mode = True

class UserRead(UserBase):
    ...
    
class UserMultiRead(UserBase):
    skip: int = 0
    limit: int = 100

class UserCreate(UserBase):
    ...


class UserCreateCredentials(UserCreate):
    password: str

    @validator('password')
    def validate_password(cls, password):
        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', password):
            raise ValueError("Password must have at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character")
        return password

class UserDelete(UserBase):
    id: int
    
class UserUpdate(UserBase):
    #id: int
    ...

class UserStatistics(UserBase):
    ...

class User(UserBase):
    id: int
    email: EmailStr
    username: str
    fullname: str
    is_superuser: bool