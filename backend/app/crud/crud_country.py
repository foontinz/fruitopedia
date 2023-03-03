from sqlalchemy.orm import Session
from typing import TypeVar

from app.models import Country, Variety
from app.crud.base import CRUDBase
from app.schemas.country import CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete, CountryRequest, CountryMultiReadByFruit, CountryResponse

countryName = TypeVar('countryName', bound=str)
countryISOCode = TypeVar('countryISOCode', bound=str)

class CRUDCountry(CRUDBase[Country, CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete]):
        
    def create(self, db: Session, *, obj_in: CountryCreate) -> Country | None:
        return super().create(db, obj_in=obj_in)
    
    def read(self, db: Session, *, obj_in: CountryRead) -> Country | None:
        return super().read(db, obj_in=obj_in)
    
    def read_multi(self, db: Session, *, obj_in: CountryMultiRead) -> list[Country]:
        return super().read_multi(db, obj_in=obj_in)
    
    def read_multi_by_fruit_id(self, db: Session, *, obj_in: CountryMultiReadByFruit) -> list[Country]:

        varieties = db.query(Variety).filter(Variety.fruit_id == obj_in.fruit_id).all()
        countries = []
        [countries.extend(variety.origin_countries) for variety in varieties]

        return list(set(countries))

    def update(self, db: Session, *, obj_in: CountryUpdate) -> Country | None:
        return super().update(db, obj_in=obj_in)
    
    def delete(self, db: Session, *, obj_in: CountryDelete) -> Country | None:
        return super().delete(db, obj_in=obj_in)
    
    def read_by_name(self, db: Session, *, name: countryName) -> Country | None:
        return db.query(Country).filter(Country.name == name).first()
    
    def read_by_iso_code(self, db: Session, *, iso_code: countryISOCode) -> Country | None:
        return db.query(Country).filter(Country.iso_code == iso_code).first()

    def request_to_create(self, db: Session, *, country_body: CountryRequest) -> CountryCreate | None:
        varieties = [db.query(Variety).filter(Variety.id == variety).first() for variety in country_body.own_varieties]

        if not all(varieties):
            return None

        return CountryCreate(
            name=country_body.name,
            iso_code=country_body.iso_code,
            description=country_body.description,
            own_varieties=varieties
        )
    
    def model_to_response_body(self, db: Session, *, country: Country, detailed: bool = False) -> CountryResponse:
        country_response = CountryResponse(
            id=country.id,
            name=country.name,
            iso_code=country.iso_code,
        )
        
        if detailed:
            country_response.description = country.description
            country_response.own_varieties = [variety.id for variety in country.own_varieties]
        
        return country_response
        
    
country = CRUDCountry(Country)