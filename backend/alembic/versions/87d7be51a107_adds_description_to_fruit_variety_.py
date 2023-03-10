"""Adds description to fruit, variety, country models.

Revision ID: 87d7be51a107
Revises: 0d6f90be77c0
Create Date: 2023-02-25 02:19:39.501912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87d7be51a107'
down_revision = '0d6f90be77c0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_id', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    op.add_column('country', sa.Column('description', sa.String(), nullable=True))
    op.add_column('fruit', sa.Column('description', sa.String(), nullable=True))
    op.add_column('variety', sa.Column('decription', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('variety', 'decription')
    op.drop_column('fruit', 'description')
    op.drop_column('country', 'description')
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('fullname', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('salt', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_banned', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('is_superuser', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=False)
    op.create_index('ix_user_id', 'user', ['id'], unique=False)
    op.create_index('ix_user_email', 'user', ['email'], unique=False)
    # ### end Alembic commands ###
