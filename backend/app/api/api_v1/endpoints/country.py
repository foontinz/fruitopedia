from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import RESPONSES
from app.crud.validators.country_validators import CountryValidators
router = APIRouter()

''' GET /country/fruit/{id}'''
@router.get("/fruit/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_countries_by_fruit_id(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.MultiReadQueryParams = Depends()):

    countries = crud.country.read_multi_by_fruit_id(db, obj_in=schemas.CountryMultiReadByFruit(fruit_id=id, **params.dict()))
    
    countries_dict = schemas.CountryMultiResponse(
        countries=[crud.country.model_to_response_body(db, country=country, detailed=params.detailed) for country in countries]
        ).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=countries_dict)

''' GET /country/{id}'''
@router.get("/{id}", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_country(
    id: int,
    detailed: bool = False,
    db: Session = Depends(get_db)):
    
    country = crud.country.read(db, obj_in=schemas.CountryRead(id=id))
    if not country:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Country not found"})
    
    country_dict = crud.country.model_to_response_body(db, country=country, detailed=detailed).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=country_dict)

''' PUT /country/{id}'''
@router.put("/{id}", responses=RESPONSES["PUT"], status_code=status.HTTP_200_OK)
async def update_country(
    id: int,
    country_body: schemas.CountryRequest = Body(...),
    db: Session = Depends(get_db)):

    try:
        CountryValidators.validate_update(db, country_id=id,country_request=country_body)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message":str(e)})
    
    country_create = crud.country.request_to_create(db, country_body=country_body)
    country = crud.country.update(db, obj_in=schemas.CountryUpdate(id=id, update_to_obj=country_create))
    if not country:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message":"Error while updating country"})
    country_dict = crud.country.model_to_response_body(db, country=country, detailed=True).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_200_OK, content=country_dict)

''' DELETE /country/{id}'''
@router.delete("/{id}", responses=RESPONSES["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
    id: int,
    db: Session = Depends(get_db)):

    try: 
        CountryValidators.validate_delete(db, country_id=id)
    except ValueError as e: 
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message":str(e)})


    if crud.country.delete(db, obj_in=schemas.CountryDelete(id=id)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while deleting country"})
    
''' GET /country/'''
@router.get("/", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_countries(
    db: Session = Depends(get_db),
    params: schemas.MultiReadQueryParams = Depends()):
    
    countries = crud.country.read_multi(db, obj_in=schemas.CountryMultiRead(skip=params.skip, limit=params.limit, detailed=params.detailed))    
    countries_dict = schemas.CountryMultiResponse(
        countries=[crud.country.model_to_response_body(db, country=country, detailed=params.detailed) for country in countries]
        ).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=countries_dict)

''' POST /country/'''
@router.post("/", responses=RESPONSES["POST"], status_code=status.HTTP_201_CREATED)
async def create_country(
    country_body: schemas.CountryRequest = Body(...),
    db: Session = Depends(get_db)):
    
    try:
        CountryValidators.validate_create(db, country_request=country_body)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message":str(e)})
    
    country_create = crud.country.request_to_create(db, country_body=country_body)
    country = crud.country.create(db, obj_in=country_create)
    
    if not country:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while creating country"})
    
    country_dict = crud.country.model_to_response_body(db, country=country, detailed=True).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=country_dict)
