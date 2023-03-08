from app.crud import country, fruit, variety
from app.models import Fruit, Variety, Country
from app.crud.validators.error import ValidationError
from app.crud.crud_variety import varietyName
from app.schemas.variety import VarietyCreate, VarietyRead, VarietyMultiRead, VarietyUpdate, VarietyDelete, VarietyRequest, VarietyResponse
from app.schemas.fruit import FruitCreate, FruitRead, FruitMultiRead, FruitUpdate, FruitDelete, FruitRequest, FruitResponse
from app.schemas.country import CountryCreate, CountryRead, CountryMultiRead, CountryUpdate, CountryDelete, CountryRequest, CountryResponse

from sqlalchemy.orm import Session


class VarietyValidators:
    @staticmethod
    def _is_variety_exist(db: Session, variety_id: int) -> Variety | None:
        return variety.read(db, obj_in=VarietyRead(id=variety_id))
    
    @staticmethod
    def _is_fruit_exist(db: Session, fruit_id: int) -> Fruit | None:
        return fruit.read(db, obj_in=FruitRead(id=fruit_id))

    @staticmethod
    def _is_variety_name_exist(db: Session, name: varietyName) -> Variety | None:
        return variety.read_by_name(db, name=name)

    @staticmethod
    def _is_variety_unique(db: Session, variety: VarietyRequest) -> bool:
        if existing_variety := variety.read_by_name(db=db, name=variety.name):
            return variety.fruit == existing_variety.fruit.id
        return True

    @staticmethod
    def _are_countries_exist(db: Session, country_ids: list[int]) -> list[Country | None]:
        return [country.read(db, obj_in=CountryRead(id=variety_id)) for variety_id in country_ids]
    
    @classmethod
    def validate_update(cls, db: Session, variety_id: int, variety_request: VarietyRequest) -> None:
        if not cls._is_variety_exist(db=db, variety_id=variety_id):
            raise ValidationError(message='Variety does not exist')
        
        if not cls._is_fruit_exist(db=db, fruit_id=variety_request.fruit):
            raise ValidationError(message="Variety`s fruit does not exist")

        if (variety_existing := variety.read_by_name_and_fruit_id(
            db=db, name=variety_request.name, fruit_id=variety_request.fruit)) and variety_existing.id != variety_id:
            raise ValidationError(message='Variety with this name and fruit already exists')
    
        if not all(cls._are_countries_exist(db=db, country_ids=variety_request.origin_countries)):
            raise ValidationError(message="Not all variety's countries exist")
        
        return 
    
    @classmethod
    def validate_create(cls, db: Session, variety_request: VarietyRequest) -> None:
        if not cls._is_variety_unique(db=db, variety=variety):
            raise ValidationError(message='Variety with this name and fruit already exists')
        
        if not all(cls._are_countries_exist(db=db, country_ids=variety_request.origin_countries)):
            raise ValidationError(message="Not all variety's countries exist")
        
        return 
    
    @classmethod
    def validate_delete(cls, db: Session, variety_request: VarietyRequest) -> None:
        if not cls._is_variety_exist(db=db, variety_id=variety_request.varieties):
            raise ValidationError(message='Variety does not exist')
        
        return