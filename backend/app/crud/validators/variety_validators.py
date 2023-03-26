from app.crud import country, fruit, variety
from app.models import Fruit, Variety, Country
from app.crud.validators.error import ValidationError
from app.crud.validators.base import ValidatorsBase
from app.crud.types import varietyName, varietyId, fruitId, countryId 
from app.schemas.variety import VarietyRead, VarietyRequest
from app.schemas.fruit import FruitRead
from app.schemas.country import CountryRead


from sqlalchemy.orm import Session
from fastapi import status

class VarietyValidators(ValidatorsBase):

    ALLOWED_FIELDS = ['id', 'name', 'description', 'fruit', 'countries']
    MODEL = Variety
    
    @staticmethod
    def _is_variety_exist(db: Session, variety_id: varietyId) -> Variety | None:
        return variety.read(db, obj_in=VarietyRead(id=variety_id))
    
    @staticmethod
    def _is_fruit_exist(db: Session, fruit_id: fruitId) -> Fruit | None:
        return fruit.read(db, obj_in=FruitRead(id=fruit_id))

    @staticmethod
    def _is_variety_name_exist(db: Session, variety_name: varietyName) -> Variety | None:
        return variety.read_by_name(db, name=variety_name)

    @staticmethod
    def _is_variety_unique(db: Session, variety: VarietyRequest) -> bool:
        if existing_variety := variety.read_by_name(db=db, name=variety.name):
            return variety.fruit == existing_variety.fruit.id
        return True

    @staticmethod
    def _are_countries_exist(db: Session, country_ids: list[countryId]) -> list[Country | None]:
        return [country.read(db, obj_in=CountryRead(id=variety_id)) for variety_id in country_ids]

    @classmethod
    def validate_update(cls, db: Session, variety_id: varietyId, variety_request: VarietyRequest) -> None:
        if not cls._is_variety_exist(db=db, variety_id=variety_id):
            raise ValidationError(code=status.HTTP_404_NOT_FOUND, message='Variety does not exist')
        
        if not cls._is_fruit_exist(db=db, fruit_id=variety_request.fruit):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message="Variety`s fruit does not exist")

        if (variety_existing := variety.read_by_name_and_fruit_id(
            db=db, name=variety_request.name, fruit_id=variety_request.fruit)) and variety_existing.id != variety_id:
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Variety with this name and fruit already exists')
    
        if not all(cls._are_countries_exist(db=db, country_ids=variety_request.origin_countries)):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message="Not all variety's countries exist")
        
        return 
    
    @classmethod
    def validate_create(cls, db: Session, variety_request: VarietyRequest) -> None:
        if not cls._is_variety_unique(db=db, variety=variety):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Variety with this name and fruit already exists')
        
        if not all(cls._are_countries_exist(db=db, country_ids=variety_request.origin_countries)):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message="Not all variety's countries exist")
        
        return 
    
    @classmethod
    def validate_delete(cls, db: Session, variety_request: VarietyRequest) -> None:
        if not cls._is_variety_exist(db=db, variety_id=variety_request.varieties):
            raise ValidationError(code=status.HTTP_404_NOT_FOUND, message='Variety does not exist')
        
        return