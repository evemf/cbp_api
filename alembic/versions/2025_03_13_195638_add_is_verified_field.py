"""Add is_verified field

Revision ID: c40f8ce230aa
Revises: 471701d34f35
Create Date: 2025-03-13 19:56:38.164754+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c40f8ce230aa'
down_revision: Union[str, None] = '471701d34f35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('competitions', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('competitions', 'max_participants',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('competitions', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('competitions', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('competitions', 'competition_type',
               existing_type=postgresql.ENUM('INDIVIDUAL', 'TEAM', name='competitiontype'),
               nullable=False)
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_verified')
    op.alter_column('competitions', 'competition_type',
               existing_type=postgresql.ENUM('INDIVIDUAL', 'TEAM', name='competitiontype'),
               nullable=True)
    op.alter_column('competitions', 'end_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('competitions', 'start_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('competitions', 'max_participants',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('competitions', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
