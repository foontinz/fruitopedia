from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import RESPONSES
from app.crud.validators.error import ValidationError
from app.crud.validators.country_validators import CountryValidators
from app.crud.validators.variety_validators import VarietyValidators
from app.crud.validators.fruit_validators import FruitValidators

router = APIRouter()

''' GET /country/fruit/{id}'''
@router.get("/fruit/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_countries_by_fruit_id(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.ReadAllQueryParams = Depends()):

    try:
        FruitValidators.validate_read(db, fruit_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    countries = crud.country.read_by_fruit_id(db, id=id, obj_in=params)
    countries_dict = crud.country.model_to_multi_response_body(
        objs=countries, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=countries_dict)

''' GET /country/variety/{id}'''
@router.get("/variety/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_countries_by_variety_id(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.CountryReadByVarietyQueryParams = Depends()):

    try: 
        VarietyValidators.validate_read(db, country_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    countries = crud.country.read_by_variety_id(db, id=id, obj_in=params)
    countries_dict = crud.country.model_to_multi_response_body(
        objs=countries, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=countries_dict)


''' GET /country/{id}'''
@router.get("/{id}", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_country(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.CountryReadQueryParams = Depends()):
    
    try:
        CountryValidators.validate_read(db, country_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    country = crud.country.read(db, obj_in=schemas.CountryRead(id=id))    
    country_dict = crud.country.model_to_response_body(
        obj=country, params=params ).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=country_dict)

''' GET /country/'''
@router.get("/", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_countries(
    db: Session = Depends(get_db),
    params: schemas.CountryReadMultiQueryParams = Depends()):
    
    try:
        CountryValidators.validate_read_multi(params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    countries = crud.country.read_multi(db, obj_in=params) if params.ids else crud.country.read_all(db, obj_in=params)    
    countries_dict = crud.country.model_to_multi_response_body(
        objs=countries, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=countries_dict)

''' PUT /country/{id}'''
@router.put("/{id}", responses=RESPONSES["PUT"], status_code=status.HTTP_200_OK)
async def update_country(
    id: int,
    country_body: schemas.CountryRequest = Body(...),
    db: Session = Depends(get_db)):

    try:
        CountryValidators.validate_update(db, country_id=id,country_request=country_body)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    country_create = crud.country.request_to_create(db, country_body=country_body)
    country = crud.country.update(db, obj_in=schemas.CountryUpdate(id=id, update_to_obj=country_create))
    if not country:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message":"Error while updating country"})
    
    country_dict = crud.country.model_to_response_body(
        obj=country, params=schemas.CountryReadQueryParams()).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_200_OK, content=country_dict)

''' DELETE /country/{id}'''
@router.delete("/{id}", responses=RESPONSES["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
    id: int,
    db: Session = Depends(get_db)):

    try: 
        CountryValidators.validate_delete(db, country_id=id)
    except ValidationError as e: 
        return JSONResponse(status_code=e.code, content={"message": e.message})
    

    if crud.country.delete(db, obj_in=schemas.CountryDelete(id=id)):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while deleting country"})
    


''' POST /country/'''
@router.post("/", responses=RESPONSES["POST"], status_code=status.HTTP_201_CREATED)
async def create_country(
    country_body: schemas.CountryRequest = Body(...),
    db: Session = Depends(get_db)):
    
    try:
        CountryValidators.validate_create(db, country_request=country_body)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    country_create = crud.country.request_to_create(db, country_body=country_body)
    country = crud.country.create(db, obj_in=country_create)
    
    if not country:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while creating country"})
    
    country_dict = crud.country.model_to_response_body(
        obj=country, params=schemas.CountryReadQueryParams()).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=country_dict)
