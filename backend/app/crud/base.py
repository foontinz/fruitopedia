from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session
from copy import copy
from app.db.base_class import Base
from pydantic import BaseModel


ModelType = TypeVar("ModelType", bound=Base)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
ReadAllSchemaType = TypeVar("ReadAllSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, ReadSchemaType, ReadAllSchemaType, UpdateSchemaType, DeleteSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        self.model = model
    
    '''Create a new record in the database
    :param db: The database session
    :param obj_in: The data used to create the record
    :return: The created record
    '''
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType | None:
        db_obj = self.model(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
     
    '''Read a record from the database by id field from the schema
    :param db: The database session
    :param id: The id used to read the record
    :return: The read record
    '''
    def read(self, db: Session, *, obj_in: ReadSchemaType) -> ModelType | None:
        return db.query(self.model).filter(self.model.id == obj_in.id).first()
        

    '''Read all records from the database
    :param db: The database session
    :param skip: The number of records to skip
    :param limit: The number of records to return
    :return: The read records
    '''
    def read_all(self, db: Session, *, obj_in: ReadAllSchemaType) -> list[ModelType]:
        return db.query(self.model).offset(obj_in.skip).limit(obj_in.limit).all()

    # '''Read a record from the database by OR(at least 1 fits ) fields from the schema 
    # :param db: The database session
    # :param obj_in: The data used to read the record
    # :param or_in: The data used to read the record by OR'''
    # def read_or(self, db: Session, *, obj_in: ReadSchemaType) -> ModelType | None:
    #     criteries = [getattr(User, k) == v for k, v in obj_in.dict(exclude_unset=True, exclude_none=True).items()]
    #     return db.query(self.model).filter(or_(*criteries)).first()

    '''Update a record in the database
    :param db: The database session
    :param obj_in: The data used to update the record
    :return: The updated record
    '''
    def update(self, db: Session, *, obj_in: UpdateSchemaType) -> ModelType | None:
        db_obj = db.query(self.model).filter(self.model.id == obj_in.id).first()
        if not db_obj:
            return None
        for key, value in obj_in.update_to_obj.dict(exclude_unset=True).items():
            setattr(db_obj, key, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    '''Delete a record from the database
    :param db: The database session
    :param obj_in: The data used to delete the record
    :return: The deleted record
    '''
    def delete(self, db: Session, *, obj_in: DeleteSchemaType) -> None:
        obj = db.query(self.model).filter(self.model.id == obj_in.id).first()
        db.delete(obj)
        db.commit()
        return None