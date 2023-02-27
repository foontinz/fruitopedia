from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.utils.convertion_misc import CountryModel_to_CountryResponseBody

router = APIRouter()

''' GET /country/fruit/{id}'''
@router.get("/fruit/{id}", response_model=schemas.CountryMultiResponseBody, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def read_countries_by_fruit_id(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.MultiReadQueryParams = Depends()):

    countries = crud.country.read_multi_by_fruit_id(db, obj_in=schemas.CountryMultiReadByFruit(fruit_id=id, **params.dict()))

    
    return schemas.CountryMultiResponseBody(countries=[CountryModel_to_CountryResponseBody(country, detailed=params.detailed) for country in countries])

''' GET /country/{id}'''
@router.get("/{id}", response_model=schemas.CountryResponseBody, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def read_country(
    id: int,
    detailed: bool = False,
    db: Session = Depends(get_db)):
    country = crud.country.read(db, obj_in=schemas.CountryRead(id=id))
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    
    return CountryModel_to_CountryResponseBody(country, detailed=detailed)

''' PUT /country/{id}'''
@router.put("/{id}", response_model=schemas.CountryResponseBody, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def update_country(
    id: int,
    country_body: schemas.CountryRequestBody = Body(...),
    db: Session = Depends(get_db)):

    country_create = crud.country.CountryRequestBody_to_CountryCreate(db, country_body=country_body)
    if not country_create:
        raise HTTPException(status_code=422, detail="Varieties in country are not found")
    
    country = crud.country.update(db, obj_in=schemas.CountryUpdate(id=id, update_to_obj=country_create))
    if not country:
        raise HTTPException(status_code=400, detail="Error while updating country")
    
    return CountryModel_to_CountryResponseBody(country)

''' DELETE /country/{id}'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_country(
    id: int,
    db: Session = Depends(get_db)):
    
    if not crud.country.read(db, obj_in=schemas.CountryRead(id=id)):
        raise HTTPException(status_code=404, detail="Country not found")
    
    crud.country.delete(db, obj_in=schemas.CountryDelete(id=id))
    
''' GET /country/'''
@router.get("/", response_model=schemas.CountryMultiResponseBody, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def read_countries(
    db: Session = Depends(get_db),
    params: schemas.MultiReadQueryParams = Depends()):
    
    countries = crud.country.read_multi(db, obj_in=schemas.CountryMultiRead(skip=params.skip, limit=params.limit, detailed=params.detailed))    
    return schemas.CountryMultiResponseBody(countries=[CountryModel_to_CountryResponseBody(country, detailed=params.detailed) for country in countries])


''' POST /country/'''
@router.post("/", response_model=schemas.CountryResponseBody, response_model_exclude_unset=True, status_code=status.HTTP_201_CREATED)
async def create_country(
    country_body: schemas.CountryRequestBody = Body(...),
    db: Session = Depends(get_db)):
    
    if crud.country.read_by_name(db, name=country_body.name) or crud.country.read_by_iso_code(db, iso_code=country_body.iso_code):
        raise HTTPException(status_code=400, detail="Country is already exist")
    
    country_create = crud.country.CountryRequestBody_to_CountryCreate(db, country_body=country_body)
    if not country_create:
        return HTTPException(status_code=422, detail="Varieties in country are not found")
    
    country = crud.country.create(db, obj_in=country_create)
    if not country:
        raise HTTPException(status_code=400, detail="Error while creating country")
    
    return CountryModel_to_CountryResponseBody(country)