"""update user table

Revision ID: de7885f76d3e
Revises: 536c2ed9da12
Create Date: 2023-08-02 14:57:38.689571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de7885f76d3e'
down_revision = '536c2ed9da12'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'USER',
        sa.Column('PROFILE_PIC_URL', sa.String(length=1024), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('USER', 'PROFILE_PIC_URL')
