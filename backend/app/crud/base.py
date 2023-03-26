from typing import Generic, TypeVar, Type

from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.schemas.commons import (
    Read, ReadAll, Create, Update, Delete, 
    BaseResponse, ReadQueryParams
)

ModelType = TypeVar("ModelType", bound=Base)
ObjectSchemaType = TypeVar("ObjectSchemaType", bound=Base)

CreateSchemaType = TypeVar("CreateSchemaType", bound=Create)
ReadSchemaType = TypeVar("ReadSchemaType", bound=Read)
ReadAllSchemaType = TypeVar("ReadAllSchemaType", bound=ReadAll)
ReadMultiSchemaType = TypeVar("ReadMultiSchemaType", bound=ReadAll)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=Update)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=Delete)

ResponseSchemaType = TypeVar("ResponseSchemaType", bound=BaseResponse)
MultiResponseSchemaType = TypeVar("MultiResponseSchemaType", bound=BaseResponse)

class CRUDBase(Generic[ModelType, ObjectSchemaType, CreateSchemaType, 
                       ReadSchemaType, ReadMultiSchemaType, ReadAllSchemaType, 
                       UpdateSchemaType, DeleteSchemaType, 
                       ResponseSchemaType, MultiResponseSchemaType]):
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
        return db.query(self.model).get(obj_in.id)
        

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

    '''Read all the records from the database by ids field from the schema 
    :param db: The database session
    :param obj_in: The data used to read the record
    '''
    def read_multi(self, db: Session, *, obj_in: ReadMultiSchemaType) -> list[ModelType]:
        return db.query(self.model).filter(self.model.id.in_(obj_in.ids)).all()

    '''Update a record in the database
    :param db: The database session
    :param obj_in: The data used to update the record
    :return: The updated record
    '''
    def update(self, db: Session, *, obj_in: UpdateSchemaType) -> ModelType | None:
        db_obj = db.query(self.model).get(obj_in.id)
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
        obj = db.query(self.model).get(obj_in.id)
        db.delete(obj)
        db.commit()
        return db.query(self.model).filter(self.model.id == obj_in.id).first()
    
    '''
    Converts a Object model to Response object
    :param obj: The ORM model object to convert
    :param fields: The fields to include in the response    
    '''
    def model_to_response_body(self, *, obj: ModelType, params: ReadQueryParams) -> ResponseSchemaType:
        return ResponseSchemaType(
                data=ObjectSchemaType.construct(
            **ObjectSchemaType.from_orm(obj).dict(include=params.fields)))
    
    def model_to_multi_response_body(self, *, objs: list[ModelType], params: ReadQueryParams) -> MultiResponseSchemaType:
        return ResponseSchemaType(
                data=[
            ObjectSchemaType.construct(**ObjectSchemaType.from_orm(obj).dict(include=params.fields)) for obj in objs])