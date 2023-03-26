from sqlalchemy.orm import Session

from app.models import Fruit, Variety, Country

from app.crud.base import CRUDBase
from app.crud.types import fruitName, countryId, varietyId
from app.schemas.fruit import (
    FruitCreate, FruitUpdate, FruitDelete, 
    FruitRead, FruitReadMulti, FruitReadAll,
    FruitRequest, FruitResponse, FruitMultiResponse, 
    FruitReadByVarietyQueryParams, FruitReadByCountryQueryParams 
)
from app.schemas.fruit import Fruit as FruitSchema

class CRUDFruit(CRUDBase[Fruit, FruitSchema, FruitCreate, 
                         FruitRead, FruitReadMulti, FruitReadAll, 
                         FruitUpdate, FruitDelete, 
                         FruitResponse, FruitMultiResponse]):
    
    
    def read_by_country_id(self, db: Session, *, country_id: countryId, obj_in: FruitReadByCountryQueryParams) -> list[Fruit]:
        country = db.query(Country).filter(Country.id == country_id).first()
        fruits = set([variety.fruit for variety in country.own_varieties][obj_in.skip:obj_in.limit + obj_in.skip])
        return list(fruits)
    
    def read_by_variety_id(self, db: Session, *, variety_id: varietyId) -> Fruit | None:
        variety = db.query(Variety).filter(Variety.id == variety_id).first()
        return variety.fruit
    
    def read_by_name(self, db: Session, *, name: fruitName) -> Fruit | None:
        return db.query(Fruit).filter(self.model.name == name).first()

    def request_to_create(self, db: Session, *, fruit_body: FruitRequest) -> FruitCreate | None:
        varieties = db.query(Variety).filter(Variety.id.in_(fruit_body.varieties)).all()
        
        return FruitCreate.construct(
            name=fruit_body.name,
            description=fruit_body.description,
            varieties=varieties
        )

        
       
        
fruit = CRUDFruit(Fruit)