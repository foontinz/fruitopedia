from pydantic import PostgresDsn, BaseSettings, validator, AnyHttpUrl
from typing import Any

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Fruitopedia"
    SECRET_KEY: str = "d3f4u1t5ecr3t5tr1ng"

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str
    POSTGRES_PORT: str = "5432"

    SQLALCHEMY_URI: PostgresDsn | None = None
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None    
    SQLALCHEMY_TEST_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_URI", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT")
            )

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_real_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
    
        return f"{values.get('SQLALCHEMY_URI')}/{values.get('POSTGRES_DB')}"

    
    @validator("SQLALCHEMY_TEST_DATABASE_URI", pre=True)    
    def assemble_test_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
    
        return f"{values.get('SQLALCHEMY_URI')}/{values.get('POSTGRES_TEST_DB')}"
        

    SUPER_USER_USERNAME: str = "admin"
    SUPER_USER_EMAIL: str = "admin@admin.com"
    SUPER_USER_PASSWORD: str = "Admin123@"



    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()