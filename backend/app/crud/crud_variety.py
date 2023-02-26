from sqlalchemy.orm import Session
from typing import TypeVar

from app.models import Variety, Country, Fruit
from app.crud.base import CRUDBase
from app.schemas.variety import VarietyCreate, VarietyRead, VarietyMultiRead, VarietyUpdate, VarietyDelete, VarietyRequestBody

varietyName = TypeVar('varietyName', bound=str)

class CRUDVariety(CRUDBase[Variety, VarietyCreate, VarietyRead, VarietyMultiRead, VarietyUpdate, VarietyDelete]):
    
    def create(self, db: Session, *, obj_in: VarietyCreate) -> Variety | None:
        return super().create(db, obj_in=obj_in)
    
    def read(self, db: Session, *, obj_in: VarietyRead) -> Variety | None:
        return super().read(db, obj_in=obj_in)
    
    def read_all(self, db: Session, *, obj_in: VarietyMultiRead) -> list[Variety]:
        return super().read_all(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: VarietyUpdate) -> Variety | None:
        return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: VarietyDelete) -> Variety | None:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_name(self, db: Session, *, name: varietyName) -> Variety | None:
        return db.query(Variety).filter(Variety.name == name).first()
    
    def read_by_fruit_id(self, db: Session, *, fruit_id: int) -> list[Variety]:
        return db.query(Variety).filter(Variety.fruit_id == fruit_id).all()

    def VarietyRequestBody_to_VarietyCreate(self, db: Session, *, variety_body: VarietyRequestBody) -> VarietyCreate | None:
        origin_countries = [db.query(Country).filter(Country.id == country_id).first() for country_id in variety_body.origin_countries]
        fruit = db.query(Fruit).filter(Fruit.id == variety_body.fruit).first()

        if not all(origin_countries) or not fruit:
            return None
        
        return VarietyCreate(
            name=variety_body.name,
            description=variety_body.description,
            origin_countries=origin_countries,
            fruit=fruit
        )



variety = CRUDVariety(Variety)