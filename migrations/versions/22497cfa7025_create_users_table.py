"""create users table

Revision ID: 22497cfa7025
Revises: 
Create Date: 2023-05-26 23:10:28.853250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22497cfa7025'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('password', sa.String(255), nullable=False)
    )


def downgrade():
    op.drop_table('users')
