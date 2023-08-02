"""create constants table

Revision ID: a04ac3f7b505
Revises: de7885f76d3e
Create Date: 2023-08-02 14:58:34.456855

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a04ac3f7b505'
down_revision = 'de7885f76d3e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'CONSTANTS',
        sa.Column('ID', sa.Integer(), nullable=False),
        sa.Column('NAME', sa.String(length=50), nullable=False),
        sa.Column('VALUE', sa.String(length=1024), nullable=False),
        sa.PrimaryKeyConstraint('ID'),
        sa.UniqueConstraint('NAME')
    )


def downgrade() -> None:
    op.drop_table('CONSTANTS')
