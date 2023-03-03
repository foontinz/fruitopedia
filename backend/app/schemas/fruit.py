from pydantic import BaseModel

from app.schemas.commons import MultiReadQueryParams
from app.models import Variety 

class FruitBase(BaseModel):
    id: int | None = None

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class FruitInDB(FruitBase):
    name: str
    description: str | None 
    varieties: list[Variety]

class FruitCreate(FruitBase):
    name: str
    description: str | None = None
    varieties: list[Variety] = []

class FruitRead(FruitBase):
    id: int 
    
class FruitMultiRead(MultiReadQueryParams):
    ...

class FruitMultiReadByCountry(FruitMultiRead):
    country_id: int

class FruitUpdate(FruitBase):
    id: int
    update_to_obj: FruitCreate

class FruitDelete(FruitBase):
    id: int

class FruitRequest(BaseModel):
    name: str
    description: str | None = None
    varieties: list[int] = []

class FruitResponse(FruitBase):
    name: str
    description: str | None 
    varieties: list[int] = []

class FruitMultiResponse(BaseModel):
    fruits: list[FruitResponse]

