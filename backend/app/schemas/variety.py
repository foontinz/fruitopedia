from pydantic import BaseModel
from app.models import Country, Fruit
from app.schemas.commons import MultiReadQueryParams
class VarietyBase(BaseModel):
    id: int | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        

class VarietyInDB(VarietyBase):
    name: str
    fruit: Fruit
    description: str | None     
    origin_countries: list[Country] 

class VarietyCreate(VarietyBase):
    name: str
    fruit: Fruit
    description: str | None = None
    origin_countries: list[Country] = []

class VarietyRead(VarietyBase):
    id: int 

class VarietyMultiRead(MultiReadQueryParams):
    ...

class VarietyUpdate(VarietyBase):
    id: int
    update_to_obj: VarietyCreate

class VarietyDelete(VarietyBase):
    id: int

class VarietyRequestBody(BaseModel):
    name: str
    fruit: int
    description: str | None = None
    origin_countries: list[int] = []

class VarietyResponse(VarietyBase):
    name: str
    fruit: int
    description: str | None 
    origin_countries: list[int] = []


class VarietyMultiResponse(BaseModel):
    varieties: list[VarietyResponse]