from sqlalchemy.orm import Session

from app.models.user import User
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete, UserLoginCredentials
from app.core.security import verify_password

from typing import TypeVar

usernameStr = TypeVar('usernameStr', bound=str)
emailStr = TypeVar('emailStr', bound=str)

class CRUDUser(CRUDBase[User, UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete]):
    
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User | None:
        return super().create(db, obj_in=obj_in)
    
    def read(self, db: Session, *, obj_in: UserRead) -> User | None:
        return super().read(db, obj_in=obj_in)
    
    def read_all(self, db: Session, *, obj_in: UserMultiRead) -> list[User]:
        return super().read_all(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: UserUpdate) -> User | None:
        return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: UserDelete) -> User | None:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_email(self, db: Session, *, email: emailStr) -> User | None:
        db.query(self.model).filter(self.model.email == email).first()
    
    def read_by_username(self, db: Session, *, username: usernameStr) -> User | None:
        db.query(self.model).filter(self.model.username == username).first()
    
    def authenticate(self, db: Session, *, obj_in: UserLoginCredentials) -> User | None:
        if obj_in.username and obj_in.email:
            user_by_username = self.read_by_username(db, username=obj_in.username)
            user_by_email = self.read_by_email(db, email=obj_in.email)
        
        user_by_identifier = user_by_email if obj_in.email else user_by_username
        
        if not user_by_identifier or not verify_password(obj_in.password, user_by_identifier.hashed_password, user_by_identifier.salt):
            return None
        return user_by_identifier
    
user = CRUDUser(User)
