from sqlalchemy.orm import Session

from app.models import Variety, Country, Fruit
from app.crud.base import CRUDBase
from app.crud.types import varietyName, fruitId, countryId
from app.schemas.variety import (
    VarietyRead, VarietyReadMulti, VarietyReadAll, 
    VarietyCreate, VarietyUpdate, VarietyDelete,
    VarietyRequest, VarietyResponse, VarietyMultiResponse,
    VarietyReadByCountryQueryParams, VarietyReadByFruitQueryParams
)

from app.schemas.variety import Variety as VarietySchema
class CRUDVariety(CRUDBase[
    Variety, VarietySchema, VarietyCreate, 
    VarietyRead, VarietyReadMulti, VarietyReadAll,
    VarietyUpdate, VarietyDelete,
    VarietyResponse, VarietyMultiResponse]):
        
    def read_by_name(self, db: Session, *, name: varietyName) -> Variety | None:
        return db.query(Variety).filter(Variety.name == name).first()
    
    def read_by_fruit_id(self, db: Session, *, fruit_id: fruitId, obj_in: VarietyReadByFruitQueryParams) -> list[Variety]:
        return db.query(Variety).filter(
            Variety.fruit_id == fruit_id).all()[obj_in.skip:obj_in.limit + obj_in.skip]

    def read_by_country_id(self, db: Session, *, country_id: countryId, obj_in: VarietyReadByCountryQueryParams) -> list[Variety]:
        return db.query(Variety).filter(
            Variety.origin_countries.any(id=country_id)).all()[obj_in.skip:obj_in.limit + obj_in.skip]
    
    def read_by_name_and_fruit_id(self, db: Session, *, name: varietyName, fruit_id: fruitId) -> Variety | None:
        return db.query(Variety).filter(Variety.name == name, Variety.fruit_id == fruit_id).first()
    
    def request_to_create(self, db: Session, *, variety_body: VarietyRequest) -> VarietyCreate | None:
        origin_countries = db.query(Country).filter(Country.id.in_(variety_body.origin_countries)).all()
        fruit = db.query(Fruit).filter(Fruit.id == variety_body.fruit).first()

        return VarietyCreate(
            name=variety_body.name,
            description=variety_body.description,
            origin_countries=origin_countries,
            fruit=fruit
        )

variety = CRUDVariety(Variety)