from app.crud import country, fruit, variety
from app.crud.crud_variety import varietyName
from app.schemas.fruit import FruitCreate, FruitRead, FruitMultiRead, FruitUpdate, FruitDelete, FruitRequest, FruitResponse
from app.schemas.variety import VarietyCreate, VarietyRead, VarietyMultiRead, VarietyUpdate, VarietyDelete, VarietyRequest, VarietyResponse
from app.models import Fruit, Variety

from sqlalchemy.orm import Session

class FruitValidators:
    
    @staticmethod
    def _is_fruit_exist(db: Session, fruit_id: int) -> Fruit | None:
        return fruit.read(db, obj_in=FruitRead(id=fruit_id))
    
    @staticmethod
    def _is_fruit_name_exist(db: Session, name: varietyName) -> Fruit | None:
        return fruit.read_by_name(db, name=name)
    
    @staticmethod
    def _are_varieties_exist(db: Session, variety_ids: list[int]) -> list[Variety | None]:
        return all([variety.read(db, obj_in=VarietyRead(id=variety_id)) for variety_id in variety_ids])
    
    @classmethod
    def validate_update(cls, db: Session, fruit_id:int, fruit_request: FruitRequest) -> None:
        if not cls._is_fruit_exist(
            db=db, fruit_id=fruit_id):
            raise ValueError('Fruit does not exist')
        
        if (fruit := cls._is_fruit_name_exist(
            db=db, name=fruit_request.name)) and fruit.id != fruit_id:
                raise ValueError('Fruit with this name already exists')
        
        if not all(cls._are_varieties_exist(
            db=db, variety_ids=fruit_request.own_varieties)):
            raise ValueError('Not all varieties exist')
        
        return 
    
    @classmethod
    def validate_create(cls, db: Session, fruit_request: FruitRequest) -> None:
        if not cls._is_name_unique(
            db=db, name=fruit_request.name):
            raise ValueError('Fruit with this name already exists')
        
        if not all(cls._are_varieties_exist(
            db=db, variety_ids=fruit_request.varieties)):
            raise ValueError("Not all fruit's varieties exist")
        
        return 
    
    @classmethod
    def validate_delete(cls, db: Session, fruit_id: int) -> None:
        if not cls._is_fruit_exist(db=db, fruit_id=fruit_id):
            raise ValueError('Fruit does not exist')
        
        return