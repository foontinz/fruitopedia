from app.models import Variety, Country
from app.crud.validators.error import ValidationError
from app.schemas.variety import VarietyRead
from app.schemas.country import CountryRead, CountryRequest
from app.crud import variety, country
from app.crud.types import countryId, countryName
from app.crud.validators.base import ValidatorsBase

from sqlalchemy.orm import Session
from fastapi import status
class CountryValidators(ValidatorsBase):
    
    ALLOWED_FIELDS = ['id', 'name', 'iso_code', 'description', 'varieties']
    MODEL = Country
    
    @staticmethod
    def _is_country_exist(db: Session, country_id: countryId) -> Country | None:
        return country.read(db, obj_in=CountryRead(id=country_id))
    
    @staticmethod
    def _is_country_name_exist(db: Session, country_name: countryName) -> Country | None:
        return country.read_by_name(db, name=country_name)
    
    @staticmethod
    def _is_country_iso_exist(db: Session, iso_code: str) -> Country | None:
        return country.read_by_iso_code(db, iso_code=iso_code)

    @staticmethod
    def _are_varieties_exist(db: Session, variety_ids: list[countryId]) -> list[Variety | None]:
        return [variety.read(db, obj_in=VarietyRead(id=variety_id)) for variety_id in variety_ids]
    
    @classmethod
    def validate_update(cls, db: Session, country_id: countryId, country_request: CountryRequest) -> None:
        if not cls._is_country_exist(db=db, country_id=country_id):
            raise ValidationError(code=status.HTTP_404_NOT_FOUND, message='Country does not exist')
        
        if (country_existing := country.read_by_name(db=db, name=country_request.name)) and country_existing.id != country_id:
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Country with this name already exists')
        
        if (country_existing := country.read_by_iso_code(db=db, iso_code=country_request.iso_code)) and country_existing.id != country_id:
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Country with this iso code already exists')
        
        if not all(cls._are_varieties_exist(db=db, variety_ids=country_request.own_varieties)):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message="Not all country's varieties exist")
        
        return
    
    @classmethod
    def validate_create(cls, db: Session, country_request: CountryRequest) -> None:
        if cls._is_country_name_exist(db=db, country_name=country_request.name):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Country with this name already exists')
        
        if cls._is_country_iso_exist(db=db, iso_code=country_request.iso_code):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Country with this iso code already exists')
        
        if not all(cls._are_varieties_exist(db=db, variety_ids=country_request.own_varieties)):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message="Not all country's varieties exist")
        
        return
    
    @classmethod
    def validate_delete(cls, db: Session, country_id: int) -> None:
        if not cls._is_country_exist(db=db, country_id=country_id):
            raise ValidationError(code=status.HTTP_404_NOT_FOUND, message='Country does not exist')
        
        return
    