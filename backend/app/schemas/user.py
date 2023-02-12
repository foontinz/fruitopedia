from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    id: int | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    hashed_password: str | None = None
    salt: str | None = None   
    is_superuser: bool = False
    is_banned: bool = False

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: EmailStr
    full_name: str
    password: str


class UserDelete(UserBase):
    # id: int
    ...

class UserUpdate(UserBase):
    # id: int
    ...


class UserStatistics(UserBase):
    ...
