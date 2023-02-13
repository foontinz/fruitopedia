from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None
    admin: bool | None = None
    exp: int | None = None
