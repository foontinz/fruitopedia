from pydantic import BaseModel, validator
from app.models import Fruit as FruitModel
from app.models import Variety as VarietyModel
from app.models import Country as CountryModel
from app.schemas.commons import (
    Read, ReadAll, ReadMulti, Create, Update, Delete,
    ReadQueryParams, ReadAllQueryParams, ReadMultiQueryParams,
    BaseResponse)

class VarietyBase(BaseModel):
    id: int | None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        
class VarietyCreate(Create):
    name: str
    fruit: FruitModel
    description: str | None = None
    origin_countries: list[CountryModel] = []

class VarietyRead(Read):
    ...

class VarietyReadMulti(ReadMulti):
    ...

class VarietyReadAll(ReadAll):
    ...

class VarietyUpdate(Update):
    update_to_obj: VarietyCreate

class VarietyDelete(Delete):
    ...

class VarietyRequest(BaseModel):
    name: str
    fruit: int
    description: str | None = None
    origin_countries: list[int] = []

    @validator("description")
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError("Description cannot be less than 10 characters")
        return v

    @validator("name", always=True)
    def validate_name(cls, v):
        if v == "":
            raise ValueError("Name cannot be empty")
        if len(v) > 50:
            raise ValueError("Name cannot be more than 50 characters")
        return v
    

class VarietyReadQueryParams(ReadQueryParams):
    ...    


class VarietyReadAllQueryParams(ReadAllQueryParams):
    ...


class VarietyReadMultiQueryParams(ReadMultiQueryParams):
    ...

class VarietyReadByFruitQueryParams(VarietyReadAllQueryParams):
    ...

class VarietyReadMultiByFruitQueryParams(VarietyReadMultiQueryParams):
    ...

class VarietyReadByCountryQueryParams(VarietyReadQueryParams):
    ...

class VarietyReadMultiByCountryQueryParams(VarietyReadMultiQueryParams):
    ...


class Variety(VarietyBase):
    name: str | None
    fruit: int | None
    description: str | None 
    origin_countries: list 

class VarietyResponse(BaseResponse):
    data: Variety | None 

class VarietyMultiResponse(BaseResponse):
    data: list[Variety]


