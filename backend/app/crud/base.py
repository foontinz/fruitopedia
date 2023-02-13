from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from app.db.base_class import Base
from pydantic import BaseModel


ModelType = TypeVar("ModelType", bound=Base)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
MultiReadSchemaType = TypeVar("MultiReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, ReadSchemaType, MultiReadSchemaType, UpdateSchemaType, DeleteSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
    
    '''Create a new record in the database
    :param db: The database session
    :param obj_in: The data used to create the record
    :return: The created record
    '''
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
     
    '''Read a record from the database
    :param db: The database session
    :param obj_in: The data used to read the record
    :return: The read record
    '''
    def read(self, db: Session, *, obj_in: ReadSchemaType) -> ModelType:
        return db.query(self.model).filter_by(**obj_in.dict()).first()
        

    '''Read multiple records from the database
    :param db: The database session
    :param obj_in: The data used to read the records
    :return: The read records
    '''
    def read_multi(self, db: Session, *, obj_in: MultiReadSchemaType) -> list[ModelType]:
        return db.query(self.model).filter_by(**obj_in.dict()).offset(obj_in.skip).limit(obj_in.limit).all()

    '''Update a record in the database
    :param db: The database session
    :param obj_in: The data used to update the record
    :return: The updated record
    '''
    def update(self, db: Session, *, obj_in: UpdateSchemaType) -> ModelType:
        db_obj = db.query(self.model).get(obj_in.id)
        db_obj.update(obj_in.dict(exclude_unset=True)) 
        db.commit()
        db.refresh(db_obj)
        return db_obj

    '''Delete a record from the database
    :param db: The database session
    :param obj_in: The data used to delete the record
    :return: The deleted record
    '''
    def delete(self, db: Session, *, obj_in: DeleteSchemaType) -> ModelType:
        obj = db.query(self.model).filter_by(**obj_in.dict()).first()
        db.delete(obj)
        db.commit()
        return obj