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

class UserCreate(UserInDB):
    fullname: str = None
    is_banned: bool = False
    is_superuser: bool = False

class UserRead(UserBase):
    email: EmailStr | None = None
    username: str | None = None 
    fullname: str | None = None
    is_banned: bool | None = None
    is_superuser: bool | None = None
    
    
class UserMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100
    read_criterias: UserRead

class UserUpdate(BaseModel):
    obj_to_update: UserRead
    update_to_obj: UserCreate


class UserDelete(BaseModel):
    obj_to_delete: UserRead
    
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


class User(UserBase):
    id: int
    email: EmailStr
    username: str
    fullname: str
    is_superuser: bool

class UserStatistics(UserBase):
    ... 

