"""init tables

Revision ID: 66f84a686e68
Revises: 
Create Date: 2023-06-18 21:20:56.994993

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66f84a686e68'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'USER',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('USERNAME', sa.String(length=50), nullable=False),
        sa.Column('HASHED_PASSWORD', sa.String(length=1024), nullable=True),
        sa.Column('HASH_SALT', sa.String(length=1024), nullable=True),
        sa.Column('IS_ACTIVE', sa.Boolean, nullable=True),
        sa.Column('CREATED_AT', sa.DateTime(timezone=True), nullable=True),
        sa.Column('UPDATED_AT', sa.DateTime(timezone=True), nullable=True, server_onupdate=sa.text('NOW()'))
    )

    op.create_table(
        'ROLE',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('NAME', sa.String(length=1024), nullable=False)
    )

    op.create_table(
        'USER_ROLE',
        sa.Column('USER_ID', sa.Integer, sa.ForeignKey('USER.ID'), primary_key=True),
        sa.Column('ROLE_ID', sa.Integer, sa.ForeignKey('ROLE.ID'), primary_key=True)
    )

    op.create_table(
        'EVENT_TYPE',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('NAME', sa.String(length=1024), nullable=False),
        sa.Column('DESCRIPTION', sa.String(length=1024), nullable=True)
    )

    op.create_table(
        'ROLE_EVENT_TYPE',
        sa.Column('ROLE_ID', sa.Integer, sa.ForeignKey('ROLE.ID'), primary_key=True),
        sa.Column('EVENT_TYPE_ID', sa.Integer, sa.ForeignKey('EVENT_TYPE.ID'), primary_key=True),
        sa.Column('CAN_EDIT', sa.Boolean, default=False),
        sa.Column('CAN_SEE', sa.Boolean, default=False),
        sa.Column('CAN_ADD', sa.Boolean, default=False)
    )

    op.create_table(
        'EVENT',
        sa.Column('ID', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('CREATED_BY', sa.Integer, sa.ForeignKey('USER.ID'), nullable=False),
        sa.Column('EVENT_TYPE', sa.Integer, sa.ForeignKey('EVENT_TYPE.ID'), nullable=False),
        sa.Column('TITLE', sa.String(length=1024), nullable=False),
        sa.Column('DESCRIPTION', sa.String(length=1024), nullable=True),
        sa.Column('START_DATE', sa.String(length=1024), nullable=False),
        sa.Column('END_DATE', sa.String(length=1024), nullable=False),
        sa.Column('CREATED_AT', sa.DateTime(timezone=True), nullable=True),
        sa.Column('UPDATED_AT', sa.DateTime(timezone=True), nullable=True, server_onupdate=sa.text('NOW()'))
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('EVENT')
    op.drop_table('ROLE_EVENT_TYPE')
    op.drop_table('EVENT_TYPE')
    op.drop_table('USER_ROLE')
    op.drop_table('ROLE')
    op.drop_table('USER')
    # ### end Alembic commands ###
