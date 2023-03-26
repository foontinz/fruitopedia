from app.crud.validators.error import ValidationError
from app.schemas import ReadQueryParams, ReadMultiQueryParams
from app.crud.base import Base

from sqlalchemy.orm import Session
from fastapi import status


class ValidatorsBase:
    
    @classmethod
    def _are_fields_allowed(cls, fields: list[str], allowed_fields: list[str] = []) -> None:
        if not allowed_fields:
            allowed_fields = cls.ALLOWED_FIELDS  
        
        if not all(field in allowed_fields for field in fields):
            raise ValidationError(code=status.HTTP_400_BAD_REQUEST, message='Invalid fields')
        
        return


    @classmethod
    def validate_read(
        cls, db: Session, 
        id: int, params: ReadQueryParams) -> None:
    
        cls._are_fields_allowed(fields=params.fields)
    
        if not db.query(cls.MODEL).filter(cls.MODEL.id == id).first():
            raise ValidationError(code=status.HTTP_404_NOT_FOUND, message='Object does not exist')
        return    


    @classmethod
    def validate_read_multi(
        cls, 
        params: ReadMultiQueryParams) -> None:
    
        cls._are_fields_allowed(fields=params.fields)
        
        
        return