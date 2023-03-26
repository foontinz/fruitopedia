from pydantic import BaseModel

class Read(BaseModel):
    id: int

class ReadAll(BaseModel):
    skip: int = 0
    limit: int = 100

class ReadMulti(BaseModel):
    ids: list[int] = []

class Create(BaseModel):
    ...

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

class Update(BaseModel):
    id: int
    update_to_obj: Create

class Delete(BaseModel):
    id: int

class ReadQueryParams(BaseModel):
    fields: list[str] = []

class ReadAllQueryParams(ReadQueryParams, ReadAll):
    ...

class ReadMultiQueryParams(ReadAllQueryParams, ReadMulti):
    ...

class BaseResponse(BaseModel):
    message: str = "Success"

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True