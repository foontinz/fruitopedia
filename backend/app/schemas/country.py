from pydantic import BaseModel, validator

from app.models import Variety as VarietyModel
from app.schemas.commons import (
    Read, ReadAll, ReadMulti, Create, Update, Delete,
    ReadQueryParams, ReadAllQueryParams, ReadMultiQueryParams,
    BaseResponse)



class CountryBase(BaseModel):
    id: int | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        
class CountryCreate(Create):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[VarietyModel] = []

class CountryRead(Read):
    id: int | None = None   
    iso_code: str | None = None

class CountryReadAll(ReadAll):
    ...

class CountryReadMulti(ReadMulti):
    ...

class CountryUpdate(Update):
    update_to_obj: CountryCreate

class CountryDelete(Delete):
    ...

class CountryRequest(BaseModel):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[int] = []

    @validator('iso_code')
    def iso_code_must_be_3_chars(cls, v):
        if len(v) != 3:
            raise ValueError('iso_code must be 3 characters long')
        return v
    
    @validator("description")
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError("Description cannot be less than 10 characters")
        return v
    
class CountryReadQueryParams(ReadQueryParams):
    ...

class CountryReadMultiQueryParams(ReadMultiQueryParams):
    ...

class CountryReadAllQueryParams(ReadAllQueryParams):
    ...

class CountryReadByFruitQueryParams(CountryReadQueryParams):
    ...

class CountryReadByFruitQueryParams(CountryReadAllQueryParams):
    ...

class CountryReadMultiByFruitQueryParams(CountryReadMultiQueryParams):
    ...

class CountryReadByVarietyQueryParams(CountryReadAllQueryParams):
    ...

class CountryReadMultiByVarietyQueryParams(CountryReadMultiQueryParams):
    ...

class Country(CountryBase):
    name: str | None 
    iso_code: str | None
    description: str | None 
    own_varieties: list

class CountryResponse(BaseResponse):
    data: Country | None
    
class CountryMultiResponse(BaseResponse):
    data: list[Country]