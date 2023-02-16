from app.db.base_class import Base
from sqlalchemy import Table, Column, ForeignKey


country_variety = Table(
    'country_variety', Base.metadata,
    Column('variety_id', ForeignKey('variety.id'), primary_key=True),
    Column('country_id', ForeignKey('country.id'), primary_key=True))
