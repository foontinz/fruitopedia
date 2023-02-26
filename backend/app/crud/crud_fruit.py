from sqlalchemy.orm import Session
from typing import TypeVar

from app.models import Fruit, Variety
from app.crud.base import CRUDBase
from app.schemas.fruit import FruitCreate, FruitUpdate, FruitRead, FruitMultiRead, FruitDelete, FruitRequestBody, FruitResponseBody

fruitName = TypeVar('fruitName', bound=str)

class CRUDFruit(CRUDBase[Fruit, FruitCreate, FruitRead, FruitMultiRead, FruitUpdate, FruitDelete]):
    
    def create(self, db: Session, *, obj_in: FruitCreate) -> Fruit | None:
        return super().create(db, obj_in=obj_in)
        
    def read(self, db: Session, *, obj_in: FruitRead) -> Fruit | None:
        return super().read(db, obj_in=obj_in)
    
    def read_all(self, db: Session, *, obj_in: FruitMultiRead) -> list[Fruit]:
        return super().read_all(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: FruitUpdate) -> Fruit | None:
        return super().update(db, obj_in=obj_in)        
    
    def delete(self, db: Session, *, obj_in: FruitDelete) -> Fruit | None:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_name(self, db: Session, *, name: fruitName) -> Fruit | None:
        return db.query(Fruit).filter(self.model.name == name).first()
    
    def FruitRequestBody_to_FruitCreate(self, db: Session, *, fruit_body: FruitRequestBody) -> FruitCreate | None:
        varieties = [db.query(Variety).filter(Variety.id == variety_id).first() for variety_id in fruit_body.varieties]

        if not all(varieties):
            return None
        

        return FruitCreate(
            name=fruit_body.name,
            description=fruit_body.description,
            varieties=varieties
        )

    

fruit = CRUDFruit(Fruit)