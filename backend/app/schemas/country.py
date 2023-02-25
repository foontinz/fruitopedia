from pydantic import BaseModel
from app.models import Variety

class CountryBase(BaseModel):
    id: int 

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        


class CountryInDB(CountryBase):
    name: str
    iso_code: str
    description: str | None 
    own_varieties: list[Variety]

class CountryCreate(CountryInDB):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[Variety] = []

class CountryRead(CountryBase):
    id: int | None = None   
    iso_code: str | None = None


class CountryMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100
    read_criterias: CountryRead

class CountryUpdate(CountryBase):
    obj_to_update: CountryRead
    update_to_obj: CountryCreate

class CountryDelete(CountryBase):
    obj_to_delete: CountryRead
