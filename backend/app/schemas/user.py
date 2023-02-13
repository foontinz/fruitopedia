from pydantic import BaseModel, EmailStr, validator
from typing import Any
from bcrypt import hashpw, gensalt

class UserBase(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    fullname: str | None = None
    hashed_password: str | None = None
    salt: str | None = None   
    is_banned: bool = False
    is_superuser: bool = False

    class Config:
        orm_mode = True

class UserRead(UserBase):
    id: int
    
class UserMultiRead(UserBase):
    skip: int = 0
    limit: int = 100

class UserCreate(UserBase):
    email: EmailStr
    fullname: str
    salt: str | None = None
    password: str | None = None
    hashed_password: str | None = None

    @validator('salt', always=True, pre=True)
    def set_salt(cls, v):
        return gensalt().decode('utf-8')
    

    
    
    

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
    fullname: str
    is_superuser: bool

class UserCredentials(UserBase):
    email: EmailStr
    password: str
