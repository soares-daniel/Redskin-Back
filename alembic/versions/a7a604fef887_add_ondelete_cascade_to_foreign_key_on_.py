"""add ondelete cascade to foreign key on event

Revision ID: a7a604fef887
Revises: fe8527bdab47
Create Date: 2023-06-29 21:05:01.310207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7a604fef887'
down_revision = 'fe8527bdab47'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('EVENT') as batch_op:
        batch_op.drop_constraint('EVENT_CREATED_BY_fkey', type_='foreignkey')
        batch_op.drop_constraint('EVENT_EVENT_TYPE_fkey', type_='foreignkey')
        batch_op.create_foreign_key('EVENT_CREATED_BY_fkey', 'USER', ['CREATED_BY'], ['ID'], ondelete='CASCADE')
        batch_op.create_foreign_key('EVENT_EVENT_TYPE_fkey', 'EVENT_TYPE', ['EVENT_TYPE'], ['ID'], ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('EVENT') as batch_op:
        batch_op.drop_constraint('EVENT_CREATED_BY_fkey', type_='foreignkey')
        batch_op.drop_constraint('EVENT_EVENT_TYPE_fkey', type_='foreignkey')
        batch_op.create_foreign_key('EVENT_CREATED_BY_fkey', 'USER', ['CREATED_BY'], ['ID'])
        batch_op.create_foreign_key('EVENT_EVENT_TYPE_fkey', 'EVENT_TYPE', ['EVENT_TYPE'], ['ID'])

