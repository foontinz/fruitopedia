from pydantic import BaseModel
from app.models import Variety

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


class CountryMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100

class CountryUpdate(CountryBase):
    id: int
    update_to_obj: CountryCreate

class CountryDelete(CountryBase):
    id: int

class CountryRequestBody(BaseModel):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[int] = []

class CountryResponseBody(CountryBase):
    name: str
    iso_code: str
    description: str | None = None
    own_varieties: list[int] = []
