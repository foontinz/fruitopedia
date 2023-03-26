from sqlalchemy.orm import Session
from functools import reduce
from operator import iconcat

from app.models import Country, Variety
from app.crud.base import CRUDBase
from app.crud.types import countryName, countryISOCode, fruitId, varietyId
from app.schemas.country import (
    CountryCreate, CountryDelete, CountryUpdate,
    CountryRead, CountryReadMulti, CountryReadAll,   
    CountryReadByFruitQueryParams, CountryReadMultiByFruitQueryParams,
    CountryReadByVarietyQueryParams, CountryReadMultiByVarietyQueryParams,
    CountryRequest, CountryResponse, CountryMultiResponse
)

from app.schemas.country import Country as CountrySchema

class CRUDCountry(CRUDBase[
    Country, CountrySchema, CountryCreate, 
    CountryRead, CountryReadMulti, CountryReadAll, 
    CountryUpdate, CountryDelete,
    CountryResponse, CountryMultiResponse]):
        
  
    def read_by_fruit_id(self, db: Session, *, id: fruitId, obj_in: CountryReadByFruitQueryParams) -> list[Country]:

        varieties = db.query(Variety).filter(Variety.fruit_id == id).all()
        countries = list(set(
            reduce(iconcat, [variety.own_countries for variety in varieties], [])))[obj_in.skip:obj_in.skip + obj_in.limit]

        return countries

    def read_by_variety_id(self, db: Session, *, id: varietyId, obj_in: CountryReadByVarietyQueryParams) -> list[Country]:
        variety = db.query(Variety).filter(Variety.id == id).first()
        countries = variety.own_countries[obj_in.skip:obj_in.skip + obj_in.limit]
        return countries
    
    def read_by_name(self, db: Session, *, name: countryName) -> Country | None:
        return db.query(Country).filter(Country.name == name).first()
    
    def read_by_iso_code(self, db: Session, *, iso_code: countryISOCode) -> Country | None:
        return db.query(Country).filter(Country.iso_code == iso_code).first()

    def request_to_create(self, db: Session, *, country_body: CountryRequest) -> CountryCreate | None:
        varieties = [db.query(Variety).filter(Variety.id == variety).first() for variety in country_body.own_varieties]

        return CountryCreate(
            name=country_body.name,
            iso_code=country_body.iso_code,
            description=country_body.description,
            own_varieties=varieties
        )
    
country = CRUDCountry(Country)