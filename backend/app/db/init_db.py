from sqlalchemy.orm import Session

from app import models, schemas
from app.utils import authorization 
from app.core.config import settings
from app.crud import user 

def init_db(db: Session) -> None:
    if not user.read_by_email(db, email=settings.SUPER_USER_EMAIL):
        user_creds = schemas.UserCreateCredentials(
            email=settings.SUPER_USER_EMAIL,
            username=settings.SUPER_USER_USERNAME,
            password=settings.SUPER_USER_PASSWORD,
        )
        user_create = authorization.UserCredentials_to_UserCreate(user_creds, is_superuser=True)
        user.create(db, obj_in=user_create)