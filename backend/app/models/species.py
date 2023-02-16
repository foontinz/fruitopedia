from app.db.base_class import Base

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column

from .fruit import Fruit
from .country import Country


class Species(Base):
    __tablename__ = "species"


    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)

    origin_countries: Mapped[list["Country"]] = relationship(back_populates="own_species", cascade="all, delete-orphan", lazy="joined", passive_deletes=True)
    fruit: Mapped["Fruit"] = relationship(back_populates="species", cascade="all, delete", lazy="joined", passive_deletes=True)

    def __repr__(self):
        return f"{self.id, self.fruit.name}: {self.name}"