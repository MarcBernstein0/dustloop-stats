"""initial revision

Revision ID: ae674e14f1ff
Revises: 
Create Date: 2025-01-17 15:12:56.088109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ae674e14f1ff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('move_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('move_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('section', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('input', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('damage', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('guard', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('startup', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('active', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('recovery', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('on_block', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('on_hit', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('level', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('counter_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('invuln', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('proration', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('risc_gain', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('risc_loss', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('url', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_move_data_character'), 'move_data', ['character'], unique=False)
    op.create_index(op.f('ix_move_data_move_type'), 'move_data', ['move_type'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_move_data_move_type'), table_name='move_data')
    op.drop_index(op.f('ix_move_data_character'), table_name='move_data')
    op.drop_table('move_data')
    # ### end Alembic commands ### 