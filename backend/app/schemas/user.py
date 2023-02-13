from pydantic import BaseModel, EmailStr, validator
from bcrypt import hashpw, gensalt

class UserBase(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    full_name: str | None = None
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
    full_name: str
    password: str

    @validator('salt')
    def create_salt(cls, v):
        return gensalt().decode('utf-8')
    
    @validator('hashed_password')
    def create_hashed_password(cls, v, values):
        return hashpw(values['password'].encode('utf-8'), values['salt'].encode('utf-8'))
    
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
    full_name: str
    is_superuser: bool
