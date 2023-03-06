from sqlalchemy.orm import Session
from typing import TypeVar

from app.models import Fruit, Variety, Country
from app.crud.base import CRUDBase
from app.schemas.fruit import FruitCreate, FruitUpdate, FruitRead, FruitMultiRead, FruitDelete, FruitRequest, FruitMultiReadByCountry, FruitResponse

fruitName = TypeVar('fruitName', bound=str)

class CRUDFruit(CRUDBase[Fruit, FruitCreate, FruitRead, FruitMultiRead, FruitUpdate, FruitDelete]):
    
    def create(self, db: Session, *, obj_in: FruitCreate) -> Fruit | None:
        return super().create(db, obj_in=obj_in)
        
    def read(self, db: Session, *, obj_in: FruitRead) -> Fruit | None:
        return super().read(db, obj_in=obj_in)
    
    def read_multi(self, db: Session, *, obj_in: FruitMultiRead) -> list[Fruit]:
        return super().read_multi(db, obj_in=obj_in)
    
    def read_multi_by_country_id(self, db: Session, *, obj_in: FruitMultiReadByCountry) -> list[Fruit]:
        country = db.query(Country).filter(Country.id == obj_in.country_id).first()
        fruits = set([variety.fruit for variety in country.own_varieties][obj_in.skip:obj_in.limit])
        return list(fruits)
    
    def update(self, db: Session, *, obj_in: FruitUpdate) -> Fruit | None:
        return super().update(db, obj_in=obj_in)        
    
    def delete(self, db: Session, *, obj_in: FruitDelete) -> Fruit | None:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_name(self, db: Session, *, name: fruitName) -> Fruit | None:
        return db.query(Fruit).filter(self.model.name == name).first()
    

    def request_to_create(self, db: Session, *, fruit_body: FruitRequest) -> FruitCreate | None:
        varieties = [db.query(Variety).filter(Variety.id == variety_id).first() for variety_id in fruit_body.varieties]
        
        return FruitCreate(
            name=fruit_body.name,
            description=fruit_body.description,
            varieties=varieties
        )

    def model_to_response_body(self, db: Session, *, fruit: Fruit, detailed: bool = False) -> FruitResponse:
        fruit_response = FruitResponse(
            id=fruit.id,
            name=fruit.name
        )
        if detailed:
            fruit_response.description = fruit.description
            fruit_response.varieties = [variety.id for variety in fruit.varieties]
        return fruit_response

fruit = CRUDFruit(Fruit)