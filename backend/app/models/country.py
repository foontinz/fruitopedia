from app.db.base_class import Base 
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .species import Species


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    iso_code: Mapped[str | None] = mapped_column(index=True, nullable=False)

    own_species: Mapped[list["Species"]] = relationship(back_populates="origin_countries", cascade="all, delete-orphan", lazy="joined", passive_deletes=True)


    def __repr__(self):
        return f"{self.id, self.name, self.code}"
    
