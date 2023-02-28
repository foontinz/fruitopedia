from app.schemas.user import UserCreateCredentials, UserCreate
from bcrypt import hashpw, gensalt


def UserCredentials_to_UserCreate(user: UserCreateCredentials, is_superuser: bool = False) -> UserCreate:
    salt = gensalt().decode('utf-8')
    return UserCreate(
        email=user.email,
        username=user.username,
        hashed_password=hashpw(password=user.password.encode('utf-8'),salt=salt.encode('utf-8')).decode('utf-8'),
        salt=salt,
        is_superuser=is_superuser)