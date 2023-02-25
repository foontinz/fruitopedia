from sqlalchemy.orm import Session

from app.models import Variety, Country, Fruit
from app.crud.base import CRUDBase
from app.schemas.variety import VarietyCreate, VarietyRead, VarietyMultiRead, VarietyUpdate, VarietyDelete

class CRUDVariety(CRUDBase[Variety, VarietyCreate, VarietyRead, VarietyMultiRead, VarietyUpdate, VarietyDelete]):
    
    def create(self, db: Session, *, obj_in: VarietyCreate) -> Variety | None:
        if self.is_fruit_exist(
            db, obj_in=obj_in.fruit) and self.are_countries_exist(db, obj_in=obj_in.origin_countries):
            return super().create(db, obj_in=obj_in)
    
    def read(self, db: Session, *, obj_in: VarietyRead) -> Variety | None:
        return super().read(db, obj_in=obj_in)
    
    def read_all(self, db: Session, *, obj_in: VarietyMultiRead) -> list[Variety]:
        return super().read_all(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: VarietyUpdate) -> Variety | None:
        if self.is_fruit_exist(
            db, obj_in=obj_in.update_to_obj.fruit) and self.are_countries_exist(db, obj_in=obj_in.update_to_obj.origin_countries):        
            return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: VarietyDelete) -> Variety | None:
        return super().delete(db, obj_in=obj_in)
    
    def are_countries_exist(self, *,  db:Session, obj_in = list[Country]) -> bool:
        for country in obj_in:
            if not db.query(Country).filter_by(id=country.id).first():
                return False
        return True
    
    def is_fruit_exist(self, db:Session, *, obj_in:Fruit) -> bool:
        return bool(db.query(Fruit).filter_by(id=obj_in.id).first())



variety = CRUDVariety(Variety)