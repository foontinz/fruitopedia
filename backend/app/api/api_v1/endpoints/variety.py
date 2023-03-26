from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import RESPONSES
from app.crud.validators.error import ValidationError
from app.crud.validators.variety_validators import VarietyValidators
from app.crud.validators.fruit_validators import FruitValidators
from app.crud.validators.country_validators import CountryValidators

router = APIRouter()



''' GET /variety/fruit/{id}'''
@router.get("/fruit/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_varieties_by_fruit_id(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.VarietyReadByFruitQueryParams = Depends()):

    try:
        FruitValidators.validate_read(db, fruit_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    varieties = crud.variety.read_by_fruit_id(db, id=id, obj_in=params)
    varieties_dict = crud.variety.model_to_multi_response_body(
        objs=varieties, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=varieties_dict)

''' GET /variety/country/{id}'''
@router.get("/country/{id}", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_varieties_by_country_id(
    id: int,
    db: Session = Depends(get_db),
    params: schemas.VarietyReadByCountryQueryParams = Depends()):

    try: 
        CountryValidators.validate_read(db, country_id=id, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})
    
    varieties = crud.variety.read_by_country_id(db, id=id, obj_in=params)
    varieties_dict = crud.variety.model_to_multi_response_body(
        objs=varieties, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=varieties_dict)

''' GET /variety/{id}'''
@router.get("/{id}", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_variety(
    id: int,
    params: schemas.VarietyReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    try:
        VarietyValidators.validate_read(db, variety_id=id)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    variety = crud.variety.read(db, obj_in=schemas.VarietyRead(id=id))
    variety_dict = crud.variety.model_to_response_body(
        obj=variety, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=variety_dict)

''' GET /variety/'''
@router.get("/", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_varieties(
    params: schemas.VarietyReadMultiQueryParams = Depends(),
    db: Session = Depends(get_db)):
    
    try:
        VarietyValidators.validate_read_multi(db, params=params)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    varieties = crud.variety.read_multi(db, obj_in=params) if params.fields else crud.variety.read_all(db, obj_in=params)
    varieties_dict = crud.variety.model_to_multi_response_body(
        objs=varieties, params=params).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=varieties_dict)


''' PUT /variety/{id}'''
@router.put("/{id}", responses=RESPONSES["PUT"], status_code=status.HTTP_200_OK)
async def update_variety(
    id: int,
    variety_body: schemas.VarietyRequest = Body(...),
    db: Session = Depends(get_db)):

    try:
        VarietyValidators.validate_update(db, variety_id=id, variety_request=variety_body)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    variety_create = crud.variety.request_to_create(db, variety_body=variety_body)
    variety = crud.variety.update(db, obj_in=schemas.VarietyUpdate(id=id, update_to_obj=variety_create))
    if not variety:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message":"Error while updating variety"})
    variety_dict = crud.variety.model_to_response_body(db, variety=variety, detailed=True).dict(exclude_unset=True)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content=variety_dict)

''' DELETE /variety/{id}'''
@router.delete("/{id}",responses=RESPONSES["DELETE"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_variety(
    id: int,
    db: Session = Depends(get_db)):

    try:
        VarietyValidators.validate_delete(db, variety_id=id)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    if crud.variety.delete(db, obj_in=schemas.VarietyDelete(id=id)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while deleting variety"})    

''' POST /variety/'''
@router.post("/", responses=RESPONSES["POST"], status_code=status.HTTP_201_CREATED)
async def create_variety(
    variety_body: schemas.VarietyRequest = Body(...),
    db: Session = Depends(get_db)):

    try:
        VarietyValidators.validate_create(db, variety_request=variety_body)
    except ValidationError as e:
        return JSONResponse(status_code=e.code, content={"message": e.message})

    variety_create = crud.variety.request_to_create(db, variety_body=variety_body)
    variety = crud.variety.create(db, obj_in=variety_create)
    if not variety:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while creating variety"})
    variety_dict = crud.variety.model_to_response_body(db, variety=variety, detailed=True).dict(exclude_unset=True)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=variety_dict)
