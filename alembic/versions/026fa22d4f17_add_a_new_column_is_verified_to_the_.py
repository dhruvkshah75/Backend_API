"""Add a new column is_verified to the users table

Revision ID: 026fa22d4f17
Revises: f3627bab6ad0
Create Date: 2025-11-21 21:12:20.835049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '026fa22d4f17'
down_revision: Union[str, Sequence[str], None] = 'f3627bab6ad0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('is_verified', sa.Boolean(), server_default='False'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_verified')
    pass
