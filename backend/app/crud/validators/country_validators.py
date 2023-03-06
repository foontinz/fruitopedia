from sqlalchemy.orm import Session

from app.models import Fruit, Variety, Country
from app.schemas.fruit import FruitRead
from app.schemas.variety import VarietyRead, VarietyRequest
from app.schemas.country import CountryRead, CountryRequest
from app.crud import fruit, variety, country


class CountryValidators:
    @staticmethod
    def _is_country_exist(db: Session, country_id: int) -> Country | None:
        return country.read(db, obj_in=CountryRead(id=country_id))
    
    @staticmethod
    def _is_country_name_exist(db: Session, name: str) -> Country | None:
        return country.read_by_name(db, name=name)
    
    @staticmethod
    def _is_country_iso_exist(db: Session, iso_code: str) -> Country | None:
        return country.read_by_iso_code(db, iso_code=iso_code)

    @staticmethod
    def _are_varieties_exist(db: Session, variety_ids: list[int]) -> list[Variety | None]:
        return [variety.read(db, obj_in=VarietyRead(id=variety_id)) for variety_id in variety_ids]

    @classmethod
    def validate_update(cls, db: Session, country_id: int, country_request: CountryRequest) -> None:
        if not cls._is_country_exist(db=db, country_id=country_id):
            raise ValueError('Country does not exist')
        

        if (country_existing := country.read_by_name(db=db, name=country_request.name)) and country_existing.id != country_id:
            raise ValueError('Country with this name already exists')
        
        if (country_existing := country.read_by_iso_code(db=db, iso_code=country_request.iso_code)) and country_existing.id != country_id:
            raise ValueError('Country with this iso code already exists')
        
        if not all(cls._are_varieties_exist(db=db, variety_ids=country_request.own_varieties)):
            raise ValueError("Not all country's varieties exist")
        
        return
    
    @classmethod
    def validate_create(cls, db: Session, country_request: CountryRequest) -> None:
        if cls._is_country_name_exist(db=db, name=country_request.name):
            raise ValueError('Country with this name already exists')
        
        if cls._is_country_iso_exist(db=db, iso_code=country_request.iso_code):
            raise ValueError('Country with this iso code already exists')
        
        if not all(cls._are_varieties_exist(db=db, variety_ids=country_request.own_varieties)):
            raise ValueError("Not all country's varieties exist")
        
        return
    
    @classmethod
    def validate_delete(cls, db: Session, country_id: int) -> None:
        if not cls._is_country_exist(db=db, country_id=country_id):
            raise ValueError('Country does not exist')
        
        return
    