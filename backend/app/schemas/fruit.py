from pydantic import BaseModel
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
    
class FruitMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100

class FruitUpdate(FruitBase):
    id: int
    update_to_obj: FruitCreate

class FruitDelete(FruitBase):
    id: int

class FruitRequestBody(BaseModel):
    name: str
    description: str | None = None
    varieties: list[int] = []

class FruitResponseBody(FruitBase):
    name: str
    description: str | None = None
    varieties: list[int] = []