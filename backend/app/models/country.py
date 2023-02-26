from app.db.base_class import Base 
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

# from .variety import Variety

class Country(Base):
    __tablename__ = 'country'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    iso_code: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    own_varieties: Mapped[list["Variety"]] = relationship(
        'Variety', secondary='country_variety', back_populates='origin_countries')

    def __repr__(self):
        return f'<Country {self.name}, iso {self.iso_code}, varieties {self.own_varieties}>'
