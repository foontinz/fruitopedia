from sqlalchemy.orm import Session

from app.models import Country, Variety
from app.crud.base import CRUDBase
from app.schemas.country import CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete

class CRUDCountry(CRUDBase[Country, CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete]):
        
    def create(self, db: Session, *, obj_in: CountryCreate) -> Country | None:
        if self.are_varieties_exist(db, obj_in=obj_in.own_varieties):
            return super().create(db, obj_in=obj_in)
    
    def read(self, db: Session, *, obj_in: CountryRead) -> Country | None:
        return super().read(db, obj_in=obj_in)
    
    def read_multi(self, db: Session, *, obj_in: CountryMultiRead) -> list[Country]:
        return super().read_multi(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: CountryUpdate) -> Country | None:
        if self.are_varieties_exist(db, obj_in=obj_in.update_to_obj.own_varieties):
            return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: CountryDelete) -> Country | None:
        return super().delete(db, obj_in=obj_in)
    
    def are_varieties_exist(self, db:Session, *, obj_in:list[Variety]) -> bool:
        for variety in obj_in:
            if not db.query(Variety).filter_by(id=variety.id):
                return False
        return True

    
country = CRUDCountry(Country)