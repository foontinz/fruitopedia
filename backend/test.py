from app.db.base_class import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base
from sqlalchemy import engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
# from .variety import Variety

Base = declarative_base()
class FakeFruit(BaseModel):
    name: str
    varieties: list[int] = []

class Fruit(Base):
    __tablename__ = 'fruit'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    varieties: Mapped[list["Variety"]] = relationship(
        'Variety', back_populates='fruit')
    
    def __repr__(self):
        return f'<Fruit {self.name}, varieties {[variety.name for variety in self.varieties]}>'



class Variety(Base):
    __tablename__ = 'variety'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()

    fruit_id: Mapped[int] = mapped_column(ForeignKey('fruit.id'))
    fruit: Mapped["Fruit"] = relationship('Fruit', back_populates='varieties')

    def __repr__(self):
        return f'<Variety {self.name}, fruit {self.fruit.name}`>'


eng = engine.create_engine('sqlite:///:memory:')
Base.metadata.create_all(eng)
Session = sessionmaker(bind=eng)

with Session() as session:
    fruit = Fruit(name='apple')
    fruit2 = Fruit(name='banana')
    variety = Variety(name='red delicious', fruit=fruit)
    variety2 = Variety(name='green delicious', fruit=fruit)
    session.add_all([fruit, fruit2, variety, variety2])
    session.commit()

    print(session.query(Fruit).filter_by(id=fruit.id).first())