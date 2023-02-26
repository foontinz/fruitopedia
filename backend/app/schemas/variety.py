from pydantic import BaseModel
from app.models import Country, Fruit

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

class VarietyMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100

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

class VarietyResponseBody(VarietyBase):
    name: str
    fruit: int
    description: str | None = None
    origin_countries: list[int] = []