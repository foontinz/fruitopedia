from sqlalchemy.orm import Session
from typing import TypeVar

from app.models import Country, Variety
from app.crud.base import CRUDBase
from app.schemas.country import CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete, CountryRequestBody

countryName = TypeVar('countryName', bound=str)
countryISOCode = TypeVar('countryISOCode', bound=str)

class CRUDCountry(CRUDBase[Country, CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete]):
        
    def create(self, db: Session, *, obj_in: CountryCreate) -> Country | None:
        return super().create(db, obj_in=obj_in)
    
    def read(self, db: Session, *, obj_in: CountryRead) -> Country | None:
        return super().read(db, obj_in=obj_in)
    
    def read_all(self, db: Session, *, obj_in: CountryMultiRead) -> list[Country]:
        return super().read_all(db, obj_in=obj_in)
    
    def update(self, db: Session, *, obj_in: CountryUpdate) -> Country | None:
        return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: CountryDelete) -> Country | None:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_name(self, db: Session, *, name: countryName) -> Country | None:
        return db.query(Country).filter(Country.name == name).first()
    
    def read_by_iso_code(self, db: Session, *, iso_code: countryISOCode) -> Country | None:
        return db.query(Country).filter(Country.iso_code == iso_code).first()

    def CountryRequestBody_to_CountryCreate(self, db: Session, *, country_body: CountryRequestBody) -> CountryCreate | None:
        varieties = [db.query(Variety).filter(Variety.id == variety).first() for variety in country_body.own_varieties]

        if not all(varieties):
            return None

        return CountryCreate(
            name=country_body.name,
            iso_code=country_body.iso_code,
            description=country_body.description,
            own_varieties=varieties
        )
        


    
country = CRUDCountry(Country)