from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import RESPONSES
from app.crud.validators.error import ValidationError
from app.crud.validators.fruit_validators import FruitValidators
from app.crud.validators.country_validators import CountryValidators
from app.crud.validators.variety_validators import VarietyValidators

router = APIRouter()

''' GET /fruit/country/{id}'''
@router.get("/country/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_fruits_by_country(
    id: int,
    params: schemas.FruitReadByCountryQueryParams = Depends(),
    db: Session = Depends(get_db)):

    try:
        CountryValidators.validate_read(db, country_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    fruits = crud.fruit.read_by_country_id(
        db, obj_in=schemas.FruitMultiReadByCountryQueryParams(country_id=id, **params.dict()))
    fruits_dict = crud.fruit.model_to_multi_response_body(
        objs=fruits, params=params).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_200_OK, content=fruits_dict)

''' GET /fruit/variety/{id}'''
@router.get("/variety/{id}", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_fruit_by_variety(
    id: int,
    params: schemas.FruitReadByVarietyQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    try:
        VarietyValidators.validate_read(db, variety_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    fruits = crud.fruit.read_by_variety_id(db, obj_in=schemas.FruitMultiReadByVariety(variety_id=id, **params.dict()))
    fruits_dict = crud.fruit.model_to_multi_response_body(
        objs=fruits, params=params).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_200_OK, content=fruits_dict)

''' GET /fruit/{id}'''
@router.get("/{id}", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_fruit(
    id: int,
    params: schemas.FruitReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    

    try:
        FruitValidators.validate_read(db, fruit_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    fruit = crud.fruit.read(db, obj_in=schemas.FruitRead(id=id))
    fruit_dict = crud.fruit.model_to_response_body(
        obj=fruit, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=fruit_dict)

''' GET /fruit/'''
@router.get("/", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_fruits(
    params: schemas.FruitReadMultiQueryParams = Depends(),
    db: Session = Depends(get_db)):
    

    try:
        FruitValidators.validate_read_multi(db, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    fruits = crud.fruit.read_multi(db, obj_in=params) if params.ids else crud.fruit.read_all(db, obj_in=params)
    fruits_dict = crud.fruit.model_to_multi_response_body(
        objs=fruits, params=params).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_200_OK, content=fruits_dict)


''' PUT /fruit/{id}'''
@router.put("/{id}", responses=RESPONSES["PUT"], status_code=status.HTTP_200_OK)
async def update_fruit(
    id: int,
    fruit_body: schemas.FruitRequest = Body(...),
    db: Session = Depends(get_db)):
    
    try:
        FruitValidators.validate_update(db, fruit_id=id, fruit_request=fruit_body)
    except ValidationError as e:    
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    fruit_create = crud.fruit.request_to_create(db, fruit_body=fruit_body)
    fruit = crud.fruit.update(db, obj_in=schemas.FruitUpdate(id=id, update_to_obj=fruit_create))
    if not fruit:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message":"Error while updating fruit"})
    
    fruit_dict = crud.fruit.model_to_response_body(
        obj=fruit, params=schemas.FruitReadQueryParams()).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=fruit_dict)

''' DELETE /fruit/{id}'''
@router.delete("/{id}", responses=RESPONSES["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_fruit(
    id: int,
    db: Session = Depends(get_db)):

    try:
        FruitValidators.validate_delete(db, fruit_id=id)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    if crud.fruit.delete(db, obj_in=schemas.FruitDelete(id=id)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while deleting fruit"})
    
''' POST /fruit/'''
@router.post("/", responses=RESPONSES["POST"], status_code=status.HTTP_201_CREATED)
async def create_fruit(
    fruit_body: schemas.FruitRequest = Body(...),
    db: Session = Depends(get_db)):
    
    try:
        FruitValidators.validate_create(db, fruit_request=fruit_body)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    fruit_create = crud.fruit.request_to_create(db, fruit_body=fruit_body)    
    fruit = crud.fruit.create(db, obj_in=fruit_create)
    if not fruit:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while creating fruit")
    
    fruit_dict = crud.fruit.model_to_response_body(
        obj=fruit, params=schemas.FruitReadQueryParams()).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=fruit_dict)
