from fastapi import APIRouter, Depends, HTTPException, Body, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.api.responses import RESPONSES
from app.crud.validators.variety_validators import VarietyValidators
router = APIRouter()

''' GET /variety/{id}'''
@router.get("/{id}", responses=RESPONSES["GET"], status_code=status.HTTP_200_OK)
async def read_variety(
    id: int,
    detailed: bool = False,
    db: Session = Depends(get_db)):
    
    variety = crud.variety.read(db, obj_in=schemas.VarietyRead(id=id))
    if not variety:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Variety not found"})

    variety_dict = crud.variety.model_to_response_body(db, variety=variety, detailed=detailed).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=variety_dict)

''' PUT /variety/{id}'''
@router.put("/{id}", responses=RESPONSES["PUT"], status_code=status.HTTP_200_OK)
async def update_variety(
    id: int,
    variety_body: schemas.VarietyRequest = Body(...),
    db: Session = Depends(get_db)):

    try:
        VarietyValidators.validate_update(db, variety_id=id, variety_request=variety_body)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})

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
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})
    
    if crud.variety.delete(db, obj_in=schemas.VarietyDelete(id=id)):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while deleting variety"})
    
''' GET /variety/'''
@router.get("/", responses=RESPONSES["MULTI_GET"], status_code=status.HTTP_200_OK)
async def read_varieties(
    params: schemas.MultiReadQueryParams = Depends(),
    db: Session = Depends(get_db)):
    varieties = crud.variety.read_multi(db, obj_in=schemas.VarietyMultiRead(skip=params.skip, limit=params.limit, detailed=params.detailed))
    varieties_dict = schemas.VarietyMultiResponse(
        varieties=[crud.variety.model_to_response_body(db, variety=variety, detailed=params.detailed) for variety in varieties]
        ).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=varieties_dict)

''' POST /variety/'''
@router.post("/", responses=RESPONSES["POST"], status_code=status.HTTP_201_CREATED)
async def create_variety(
    variety_body: schemas.VarietyRequest = Body(...),
    db: Session = Depends(get_db)):

    try:
        VarietyValidators.validate_create(db, variety_request=variety_body)
    except ValueError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": str(e)})
    
    variety_create = crud.variety.request_to_create(db, variety_body=variety_body)
    variety = crud.variety.create(db, obj_in=variety_create)
    if not variety:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"message": "Error while creating variety"})
    
    variety_dict = crud.variety.model_to_response_body(db, variety=variety, detailed=True).dict(exclude_unset=True)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=variety_dict)
