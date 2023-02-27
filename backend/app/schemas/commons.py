from pydantic import BaseModel


class MultiReadQueryParams(BaseModel):
    skip: int = 0
    limit: int = 100
    detailed: bool = False