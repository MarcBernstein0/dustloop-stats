"""make move fields optional

Revision ID: dff5b4637832
Revises: ae674e14f1ff
Create Date: 2025-01-17 15:15:21.219252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'dff5b4637832'
down_revision: Union[str, None] = 'ae674e14f1ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('move_data', 'input',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'damage',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'guard',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'startup',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'active',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'recovery',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'on_block',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'on_hit',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'level',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'counter_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'invuln',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'proration',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'risc_gain',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('move_data', 'risc_loss',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('move_data', 'risc_loss',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'risc_gain',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'proration',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'invuln',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'counter_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'level',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'on_hit',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'on_block',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'recovery',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'active',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'startup',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'guard',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'damage',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('move_data', 'input',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ### 