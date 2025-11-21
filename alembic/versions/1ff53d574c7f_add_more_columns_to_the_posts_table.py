"""add more columns to the posts table

Revision ID: 1ff53d574c7f
Revises: ce7e0f15e70e
Create Date: 2025-11-21 14:14:50.628974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ff53d574c7f'
down_revision: Union[str, Sequence[str], None] = 'ce7e0f15e70e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column(
        'content', sa.String(), nullable=False
    ))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
