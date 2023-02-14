from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import User
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete, UserLoginCredentials
from app.core.security import verify_password

class CRUDUser(CRUDBase[User, UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete]):
    
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        return super().create(db, obj_in=UserCreate(**obj_in.dict(exclude_none=True, exclude={'password'})))
    
    def read(self, db: Session, *, obj_in: UserRead) -> User:
        return super().read(db, obj_in=UserRead(**obj_in.dict(exclude_none=True)))
    
    def read_multi(self, db: Session, *, obj_in: UserMultiRead) -> list[User]:
        return super().read_multi(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: UserUpdate) -> User:
        return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: UserDelete) -> User:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_email(self, db: Session, *, obj_in: UserRead) -> User:
        return self.read(db, obj_in=UserRead(email=obj_in.email))
    
    def read_by_username(self, db: Session, *, obj_in: UserRead) -> User:
        return self.read(db, obj_in=UserRead(username=obj_in.username))
    
    def read_by_identifier(self, db: Session, *, obj_in: UserRead) -> User:
        return self.read_or(db, obj_in=UserRead(id=obj_in.id, email=obj_in.email, username=obj_in.username))

    def authenticate(self, db: Session, *, obj_in: UserLoginCredentials) -> User:
        user = self.read_by_identifier(db, obj_in=UserRead(**obj_in.dict(exclude_none=True)))
        if not user:
            return None
        if not verify_password(obj_in.password, user.hashed_password, user.salt):
            return None
        return user
    
user = CRUDUser(User)
