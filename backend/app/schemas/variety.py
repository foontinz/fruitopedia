from pydantic import BaseModel
from app.models import Country, Fruit

class VarietyBase(BaseModel):
    id: int 

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
    id: int | None = None
    name: str | None = None

class VarietyMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100
    read_criterias: VarietyRead

class VarietyUpdate(BaseModel):
    obj_to_update: VarietyRead
    update_to_obj: VarietyCreate

class VarietyDelete(BaseModel):
    obj_to_delete: VarietyRead