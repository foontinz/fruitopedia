from app.db.base_class import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Fruit(Base):
    __tablename__ = 'fruit'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column(nullable=True)

    varieties: Mapped[list["Variety"]] = relationship(
        'Variety', back_populates='fruit')
    
    def __repr__(self):
        return f'<Fruit {self.name}, varieties {[variety.name for variety in self.varieties]}>'

