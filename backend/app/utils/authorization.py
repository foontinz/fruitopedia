from app.schemas.user import UserCreateCredentials
from bcrypt import hashpw, gensalt


def salt_hash_user_password(user: UserCreateCredentials) -> UserCreateCredentials:
    user.salt = gensalt().decode('utf-8')
    user.hashed_password = hashpw(password=user.password.encode('utf-8'), salt=user.salt.encode('utf-8')).decode('utf-8')
    return user