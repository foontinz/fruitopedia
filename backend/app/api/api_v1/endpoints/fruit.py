from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import RESPONSES
from app.crud.validators.error import ValidationError
from app.crud.validators.fruit_validators import FruitValidators

router = APIRouter()

''' GET /fruit/country/{id}'''
@router.get("/country/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_fruits_by_country(
    id: int,
    params: schemas.MultiReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    fruits = crud.fruit.read_multi_by_country_id(db, obj_in=schemas.FruitMultiReadByCountry(country_id=id, **params.dict()))
    fruits_dict = schemas.FruitMultiResponse(
        fruits=[crud.fruit.model_to_response_body(db, fruit=fruit, detailed=params.detailed) for fruit in fruits]
        ).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=fruits_dict)


''' GET /fruit/{id}'''
@router.get("/{id}", responses=RESPONSES["GET"], response_model_exclude_unset=True)
async def read_fruit(
    id: int,
    detailed: bool = False,
    db: Session = Depends(get_db)):
    
    fruit = crud.fruit.read(db, obj_in=schemas.FruitRead(id=id))
    if not fruit:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Fruit not found"})
    
    fruit_dict = crud.fruit.model_to_response_body(db, fruit=fruit, detailed=detailed).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=fruit_dict)

''' PUT /fruit/{id}'''
@router.put("/{id}", responses=RESPONSES["PUT"], status_code=status.HTTP_200_OK)
async def update_fruit(
    id: int,
    fruit_body: schemas.FruitRequest = Body(...),
    db: Session = Depends(get_db)):
    
    try:
        FruitValidators.validate_update(db, id=id, fruit_request=fruit_body)
    except ValidationError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})
    
    fruit_create = crud.fruit.request_to_create(db, fruit_body=fruit_body)

    fruit = crud.fruit.update(db, obj_in=schemas.FruitUpdate(id=id, update_to_obj=fruit_create))
    if not fruit:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message":"Error while updating fruit"})
    
    fruit_dict = crud.fruit.model_to_response_body(db, fruit=fruit, detailed=True).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=fruit_dict)

''' DELETE /fruit/{id}'''
@router.delete("/{id}", responses=RESPONSES["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_fruit(
    id: int,
    db: Session = Depends(get_db)):

    try:
        FruitValidators.validate_delete(db, id=id)
    except ValidationError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})

    if crud.fruit.delete(db, obj_in=schemas.FruitDelete(id=id)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while deleting fruit"})
    
''' GET /fruit/'''
@router.get("/", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_fruits(
    params: schemas.MultiReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    fruits = crud.fruit.read_multi(db, obj_in=schemas.FruitMultiRead(query_params=params))
    fruits_dict = schemas.FruitMultiResponse(
        fruits=[crud.fruit.model_to_response_body(db, fruit=fruit, detailed=params.detailed) for fruit in fruits]
        ).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=fruits_dict)

''' POST /fruit/'''
@router.post("/", responses=RESPONSES["POST"], response_model_exclude_unset=True, status_code=status.HTTP_201_CREATED)
async def create_fruit(
    fruit_body: schemas.FruitRequest = Body(...),
    db: Session = Depends(get_db)):
    
    try:
        FruitValidators.validate_create(db, fruit_request=fruit_body)
    except ValidationError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})

    fruit_create = crud.fruit.request_to_create(db, fruit_body=fruit_body)    
    fruit = crud.fruit.create(db, obj_in=fruit_create)
    if not fruit:
        raise JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while creating fruit")
    
    fruit_dict = crud.fruit.model_to_response_body(db, fruit=fruit, detailed=True).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=fruit_dict)
