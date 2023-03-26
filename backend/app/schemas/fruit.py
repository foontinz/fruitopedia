from pydantic import BaseModel, validator
from app.models import Variety as VarietyModel
from app.schemas.commons import (
    Read, ReadAll, ReadMulti, Create, Update, Delete,
    ReadQueryParams, ReadAllQueryParams, ReadMultiQueryParams,
    BaseResponse)

class FruitBase(BaseModel):
    id: int | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class FruitCreate(Create):
    name: str
    description: str | None = None
    varieties: list[VarietyModel] = []

class FruitRead(Read):
    id: int 

class FruitReadAll(ReadAll):
    ...

class FruitReadMulti(ReadMulti):
    ...
    
class FruitUpdate(Update):
    update_to_obj: FruitCreate

class FruitDelete(Delete):
    id: int

class FruitRequest(BaseModel):
    name: str
    description: str | None = None
    varieties: list[int] = []


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

class FruitReadQueryParams(ReadQueryParams):
    ...

class FruitReadAllQueryParams(ReadAllQueryParams):
    ...

class FruitReadMultiQueryParams(ReadMultiQueryParams):
    ...

class FruitReadByCountryQueryParams(ReadAllQueryParams):
    ...

class FruitReadMultiByCountryQueryParams(ReadMultiQueryParams):
    ...

class FruitReadByVarietyQueryParams(FruitReadQueryParams):
    ...

class FruitReadMultiByVarietyQueryParams(FruitReadMultiQueryParams):
    ...

class Fruit(FruitBase):
    name: str | None
    description: str | None 
    varieties: list

class FruitResponse(BaseResponse):
    data: Fruit | None

class FruitMultiResponse(BaseResponse):
    data: list[Fruit]
    
