"""create_users_table

Revision ID: 2f955a0075e0
Revises: 
Create Date: 2025-06-08 15:33:48.854505

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f955a0075e0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column("id", sa.BigInteger(), autoincrement=False, nullable=False),
        sa.Column('username', sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('taps', sa.BigInteger(), server_default='0', nullable=False),
        sa.Column('name', sa.Text(), nullable=True),
        sa.Column('info', sa.Text(), nullable=True),
        sa.Column('photo', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')