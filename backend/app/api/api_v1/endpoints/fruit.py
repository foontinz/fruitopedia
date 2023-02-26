from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.utils.convertion_misc import FruitModel_to_FruitResponseBody


router = APIRouter()

''' GET /fruit/{id}'''
@router.get("/{id}", response_model=schemas.FruitResponseBody)
async def read_fruit(
    id: int,
    db: Session = Depends(get_db)):
    
    fruit = crud.fruit.read(db, obj_in=schemas.FruitRead(id=id))
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    
    return FruitModel_to_FruitResponseBody(fruit)

''' PUT /fruit/{id}'''
@router.put("/{id}", response_model=schemas.FruitResponseBody)
async def update_fruit(
    id: int,
    fruit_body: schemas.FruitRequestBody = Body(...),
    db: Session = Depends(get_db)):
    
    fruit_create = crud.fruit.FruitRequestBody_to_FruitCreate(db, fruit_body=fruit_body)
    if not fruit_create:
        return HTTPException(status_code=422, detail="Varieties in fruit are not found")
    
    fruit = crud.fruit.update(db, obj_in=schemas.FruitUpdate(id=id, update_to_obj=fruit_create))
    if not fruit:
        raise HTTPException(status_code=400, detail="Error while updating fruit")
    
    return FruitModel_to_FruitResponseBody(fruit)

''' DELETE /fruit/{id}'''
@router.delete("/{id}", response_model=schemas.FruitResponseBody)
async def delete_fruit(
    id: int,
    db: Session = Depends(get_db)):
    
    fruit = crud.fruit.delete(db, obj_in=schemas.FruitDelete(id=id))
    if not fruit:
        raise HTTPException(status_code=400, detail="Error while deleting fruit")
    
    return FruitModel_to_FruitResponseBody(fruit)

''' POST /fruit/'''
@router.post("/", response_model=schemas.FruitResponseBody)
async def create_fruit(
    fruit_body: schemas.FruitRequestBody = Body(...),
    db: Session = Depends(get_db)):
    
    if crud.fruit.read_by_name(db, name=fruit_body.name):
        raise HTTPException(status_code=400, detail="Fruit is already exist")
    
    fruit_create = crud.fruit.FruitRequestBody_to_FruitCreate(db, fruit_body=fruit_body)
    if not fruit_create:
        raise HTTPException(status_code=422, detail="Varieties in fruit are not found")
    

    fruit = crud.fruit.create(db, obj_in=fruit_create)
    if not fruit:
        raise HTTPException(status_code=400, detail="Error while creating fruit")
    
    return FruitModel_to_FruitResponseBody(fruit)