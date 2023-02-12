from crud.base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserRead, UserMultiRead, UserUpdate, UserDelete
from sqlalchemy.orm import Session

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
    