"""Fixed country column definition in user model

Revision ID: a85d9837c8cf
Revises: 9068f3f59a63
Create Date: 2025-03-14 09:47:20.997203+00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a85d9837c8cf'
down_revision: Union[str, None] = '9068f3f59a63'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('country', sa.String(), nullable=True))
    op.create_index(op.f('ix_users_country'), 'users', ['country'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_country'), table_name='users')
    op.drop_column('users', 'country')
    # ### end Alembic commands ###
