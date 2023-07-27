"""update user table

Revision ID: 536c2ed9da12
Revises: a7a604fef887
Create Date: 2023-08-01 20:24:43.766830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '536c2ed9da12'
down_revision = 'a7a604fef887'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'USER',
        sa.Column('FIRST_NAME', sa.String(length=50), nullable=True)
    )
    op.add_column(
        'USER',
        sa.Column('LAST_NAME', sa.String(length=50), nullable=True)
    )


def downgrade() -> None:
    op.drop_column('USER', 'FIRST_NAME')
    op.drop_column('USER', 'LAST_NAME')
