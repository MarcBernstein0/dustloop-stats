"""adds character model

Revision ID: 0ee5387f1f99
Revises: 23e6366c9f60
Create Date: 2025-01-17 15:59:11.264248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0ee5387f1f99'
down_revision: Union[str, None] = '23e6366c9f60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('display_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_characters_name'), 'characters', ['name'], unique=False)
    op.create_index(op.f('ix_characters_slug'), 'characters', ['slug'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_characters_slug'), table_name='characters')
    op.drop_index(op.f('ix_characters_name'), table_name='characters')
    op.drop_table('characters')
    # ### end Alembic commands ### 