from app.db.base import Base
from sqlalchemy import Boolean, Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    fullname = Column(String)
    hashed_password = Column(String)
    salt = Column(String)
    is_banned = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)

    def __repr__(self):
        return f"{self.id, self.email, self.is_superuser}"

