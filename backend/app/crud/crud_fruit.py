from sqlalchemy.orm import Session

from app.models import Fruit, Variety
from app.crud import variety
from app.crud.base import CRUDBase
from app.schemas.fruit import FruitCreate, FruitUpdate, FruitRead, FruitMultiRead, FruitDelete

class CRUDFruit(CRUDBase[Fruit, FruitCreate, FruitRead, FruitMultiRead, FruitUpdate, FruitDelete]):
    
    def create(self, db: Session, *, obj_in: FruitCreate) -> Fruit | None:
        if self.are_varieties_exist(db, obj_in=obj_in.varieties):    
            return super().create(db, obj_in=obj_in)
        
    def read(self, db: Session, *, obj_in: FruitRead) -> Fruit | None:
        return super().read(db, obj_in=obj_in)
    
    def read_multi(self, db: Session, *, obj_in: FruitMultiRead) -> list[Fruit]:
        return super().read_multi(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: FruitUpdate) -> Fruit | None:
        if self.are_varieties_exist(db, obj_in=obj_in.update_to_obj.varieties):
            return super().update(db, obj_in=obj_in)        
    
    def delete(self, db: Session, *, obj_in: FruitDelete) -> Fruit | None:
        return super().delete(db, obj_in=obj_in)
    
    def are_varieties_exist(self, db: Session, *, obj_in:list[Variety]) -> bool:
        for variety in obj_in:
            if not db.query(Variety).filter_by(id=variety.id).first():
                return False
        return True
    

fruit = CRUDFruit(Fruit)