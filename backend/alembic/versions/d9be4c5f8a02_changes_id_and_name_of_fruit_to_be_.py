"""Changes id and name of Fruit to be indexed and unique, changes iso_code of country to be unique

Revision ID: d9be4c5f8a02
Revises: 87d7be51a107
Create Date: 2023-02-25 23:12:27.832099

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9be4c5f8a02'
down_revision = '87d7be51a107'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'country', ['iso_code'])
    op.create_index(op.f('ix_fruit_id'), 'fruit', ['id'], unique=False)
    op.create_index(op.f('ix_fruit_name'), 'fruit', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_fruit_name'), table_name='fruit')
    op.drop_index(op.f('ix_fruit_id'), table_name='fruit')
    op.drop_constraint(None, 'country', type_='unique')
    # ### end Alembic commands ###