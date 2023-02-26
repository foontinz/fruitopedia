from pydantic import BaseModel, EmailStr, validator
import re

class UserBase(BaseModel):
    id: int | None = None
    class Config:
        orm_mode = True

class UserInDB(UserBase):
    email: EmailStr
    username: str
    fullname: str
    hashed_password: str
    salt: str
    is_banned: bool
    is_superuser: bool

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    fullname: str = None
    hashed_password: str
    salt: str
    is_banned: bool = False
    is_superuser: bool = False

class UserRead(UserBase):
    id: int 
    
class UserMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100

class UserUpdate(UserBase):
    id: int 
    update_to_obj: UserCreate


class UserDelete(UserBase):
    id: int
    
class UserCreateCredentials(BaseModel):
    email: EmailStr
    username: str 
    password: str

    
    @validator('username')
    def validate_username(cls, username):
        if not re.search(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError("Username must have only letters, numbers and underscores")
        return username
    
    @validator('email')
    def validate_email(cls, email):
        if not re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise ValueError("Email must be valid")
        return email
    
    @validator('password')
    def validate_password(cls, password):
        if not re.search(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', password):
            raise ValueError("Password must have at least 8 characters, 1 uppercase, 1 lowercase, 1 number and 1 special character")
        return password

class UserLoginCredentials(UserCreateCredentials):
    username: str | None = None
    email: EmailStr | None = None


