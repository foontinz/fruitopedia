from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db


router = APIRouter()

''' GET /fruit/country/{id}'''
@router.get("/country/{id}", response_model=schemas.FruitMultiResponse, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def read_fruits_by_country(
    id: int,
    params: schemas.MultiReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    fruits = crud.fruit.read_multi_by_country_id(db, obj_in=schemas.FruitMultiReadByCountry(country_id=id, **params.dict()))
    return schemas.FruitMultiResponse(fruits=[crud.fruit.model_to_response_body(db, fruit=fruit, detailed=params.detailed) for fruit in fruits])

''' GET /fruit/{id}'''
@router.get("/{id}", response_model=schemas.FruitResponse, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def read_fruit(
    id: int,
    detailed: bool = False,
    db: Session = Depends(get_db)):
    
    fruit = crud.fruit.read(db, obj_in=schemas.FruitRead(id=id))
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    
    return crud.fruit.model_to_response_body(db, fruit=fruit, detailed=detailed)

''' PUT /fruit/{id}'''
@router.put("/{id}", response_model=schemas.FruitResponse, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
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
    
    return crud.fruit.model_to_response_body(db, fruit=fruit)

''' DELETE /fruit/{id}'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fruit(
    id: int,
    db: Session = Depends(get_db)):
    
    crud.fruit.delete(db, obj_in=schemas.FruitDelete(id=id))
    
''' GET /fruit/'''
@router.get("/", response_model=schemas.FruitMultiResponse, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def read_fruits(
    params: schemas.MultiReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    fruits = crud.fruit.read_multi(db, obj_in=schemas.FruitMultiRead(query_params=params))
    return schemas.FruitMultiResponse(fruits=[crud.fruit.model_to_response_body(db, fruit=fruit, detailed=params.detailed) for fruit in fruits])

''' POST /fruit/'''
@router.post("/", response_model=schemas.FruitResponse, response_model_exclude_unset=True, status_code=status.HTTP_201_CREATED)
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
    
    return crud.fruit.model_to_response_body(db, fruit=fruit)