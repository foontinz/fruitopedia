from crud.base import CRUDBase
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete, UserCredentials
from app.core.security import verify_password

class CRUDUser(CRUDBase[User, UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete]):
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        return super().create(db, obj_in=obj_in)    

    def read(self, db: Session, *, obj_in: UserRead) -> User:
        return super().read(db, obj_in=obj_in)
    
    def read_multi(self, db: Session, *, obj_in: UserMultiRead) -> list[User]:
        return super().read_multi(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: UserUpdate) -> User:
        return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: UserDelete) -> User:
        return super().delete(db, obj_in=obj_in)
    
    def authenticate(self, db: Session, *, obj_in: UserCredentials) -> User:
        user = db.query(self.model).filter_by(email=obj_in.email).first()
        if not user:
            return None
        if not verify_password(obj_in.password, user.hashed_password, user.salt):
            return None
        return user
    
user = CRUDUser(User)