from app.db.base_class import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey



class Variety(Base):
    __tablename__ = 'variety'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    fruit_id: Mapped[int] = mapped_column(ForeignKey('fruit.id'))
    fruit: Mapped["Fruit"] = relationship('Fruit', back_populates='varieties')
    description: Mapped[str] = mapped_column(nullable=True)

    origin_countries: Mapped[list["Country"]] = relationship(
        'Country', secondary='country_variety', back_populates='own_varieties')
    
    def __repr__(self):
        return f'<Variety {self.name}, fruit {self.fruit.name}`>'

