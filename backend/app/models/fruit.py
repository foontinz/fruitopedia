from app.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .country import Country
from .species import Species

class Fruit(Base):
    __tablename__ = "fruits"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    
    species: Mapped["Species"] = relationship(back_populates="fruit", cascade="all, delete", lazy="joined", passive_deletes=True)


    def __repr__(self):
        return f"{self.id, self.name}"