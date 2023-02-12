from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from app.db.base_class import Base


ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Base)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Base)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=Base)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType, DeleteSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
    

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass