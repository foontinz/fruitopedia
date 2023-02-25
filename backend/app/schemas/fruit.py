from pydantic import BaseModel
from app.models import Variety 

class FruitBase(BaseModel):
    id: int 

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class FruitInDB(FruitBase):
    name: str
    description: str | None = None
    varieties: list[Variety]

class FruitCreate(FruitBase):
    name: str
    description: str | None = None
    varieties: list[Variety] = []

class FruitRead(FruitBase):
    id: int | None = None
    name: str | None = None

class FruitMultiRead(BaseModel):
    skip: int = 0
    limit: int = 100
    read_criterias: FruitRead

class FruitUpdate(FruitBase):
    obj_to_update: FruitRead
    update_to_obj: FruitCreate

class FruitDelete(FruitBase):
    obj_to_delete: FruitRead