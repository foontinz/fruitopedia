from pydantic import BaseModel, validator

from app.models import Variety
from app.schemas.commons import MultiReadQueryParams

class CountryBase(BaseModel):
    id: int | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        
class CountryInDB(CountryBase):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[Variety]

class CountryCreate(CountryBase):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[Variety] = []

class CountryRead(CountryBase):
    id: int | None = None   
    iso_code: str | None = None


class CountryMultiRead(MultiReadQueryParams):
    ...

class CountryMultiReadByFruit(CountryMultiRead):
    fruit_id: int

class CountryUpdate(CountryBase):
    id: int
    update_to_obj: CountryCreate

class CountryDelete(CountryBase):
    id: int

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
    
class CountryResponse(CountryBase):
    name: str
    iso_code: str
    description: str | None 
    own_varieties: list[int] = []


class CountryMultiResponse(BaseModel):
    countries: list[CountryResponse]