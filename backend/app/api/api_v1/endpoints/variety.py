from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api.deps import get_db
from app.utils.convertion_misc import VarietyModel_to_VarietyResponseBody

router = APIRouter()

''' GET /variety/{id}'''
@router.get("/{id}", response_model=schemas.VarietyResponseBody, status_code=status.HTTP_200_OK)
async def read_variety(
    id: int,
    detailed: bool = False,
    db: Session = Depends(get_db)):
    
    variety = crud.variety.read(db, obj_in=schemas.VarietyRead(id=id))
    if not variety:
        raise HTTPException(status_code=404, detail="Variety not found")
    
    return VarietyModel_to_VarietyResponseBody(variety, detailed=detailed)

''' PUT /variety/{id}'''
@router.put("/{id}", response_model=schemas.VarietyResponseBody, status_code=status.HTTP_200_OK)
async def update_variety(
    id: int,
    variety_body: schemas.VarietyRequestBody = Body(...),
    db: Session = Depends(get_db)):
    
    variety_create = crud.variety.VarietyRequestBody_to_VarietyCreate(db, variety_body=variety_body)
    if not variety_create:
        raise HTTPException(status_code=422, detail="Fruit or countries for variety are not found")
    
    variety = crud.variety.update(db, obj_in=schemas.VarietyUpdate(id=id, update_to_obj=variety_create))
    if not variety:
        raise HTTPException(status_code=400, detail="Error while updating variety")
    
    return VarietyModel_to_VarietyResponseBody(variety)

''' Delete /variety/{id}'''
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_variety(
    id: int,
    db: Session = Depends(get_db)):


    if not crud.variety.read(db, obj_in=schemas.VarietyRead(id=id)):
        raise HTTPException(status_code=404, detail="Variety not found")
    
    crud.variety.delete(db, obj_in=schemas.VarietyDelete(id=id))
    
''' GET /variety/'''
@router.get("/", response_model=schemas.VarietyMultiResponseBody, status_code=status.HTTP_200_OK)
async def read_varieties(
    params: schemas.MultiReadQueryParams = Depends(),
    db: Session = Depends(get_db)):

    varieties = crud.variety.read_multi(db, obj_in=schemas.VarietyMultiRead(skip=params.skip, limit=params.limit, detailed=params.detailed))
    return schemas.VarietyMultiResponseBody(varieties=[VarietyModel_to_VarietyResponseBody(variety, detailed=params.detailed) for variety in varieties])

''' POST /variety/'''
@router.post("/", response_model=schemas.VarietyResponseBody, status_code=status.HTTP_201_CREATED)
async def create_variety(
    variety_body: schemas.VarietyRequestBody = Body(...),
    db: Session = Depends(get_db)):

    if crud.variety.read_by_name(db, name=variety_body.name) in crud.variety.read_by_fruit_id(db, fruit_id=variety_body.fruit):
        raise HTTPException(status_code=400, detail="Variety is already exist")
    
    variety_create = crud.variety.VarietyRequestBody_to_VarietyCreate(db, variety_body=variety_body)
    if not variety_create:
        raise HTTPException(status_code=422, detail="Fruit or countries for variety are not found")
    
    variety = crud.variety.create(db, obj_in=variety_create)
    if not variety:
        raise HTTPException(status_code=400, detail="Error while creating variety")
    
    return VarietyModel_to_VarietyResponseBody(variety)
