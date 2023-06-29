"""add ondelete cascade to foreign keys

Revision ID: fe8527bdab47
Revises: d0a2e9f40e01
Create Date: 2023-06-29 21:03:41.963856

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe8527bdab47'
down_revision = 'd0a2e9f40e01'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('USER_ROLE') as batch_op:
        batch_op.drop_constraint('USER_ROLE_USER_ID_fkey', type_='foreignkey')
        batch_op.drop_constraint('USER_ROLE_ROLE_ID_fkey', type_='foreignkey')
        batch_op.create_foreign_key('USER_ROLE_USER_ID_fkey', 'USER', ['USER_ID'], ['ID'], ondelete='CASCADE')
        batch_op.create_foreign_key('USER_ROLE_ROLE_ID_fkey', 'ROLE', ['ROLE_ID'], ['ID'], ondelete='CASCADE')

    with op.batch_alter_table('ROLE_EVENT_TYPE') as batch_op:
        batch_op.drop_constraint('ROLE_EVENT_TYPE_ROLE_ID_fkey', type_='foreignkey')
        batch_op.drop_constraint('ROLE_EVENT_TYPE_EVENT_TYPE_ID_fkey', type_='foreignkey')
        batch_op.create_foreign_key('ROLE_EVENT_TYPE_ROLE_ID_fkey', 'ROLE', ['ROLE_ID'], ['ID'], ondelete='CASCADE')
        batch_op.create_foreign_key('ROLE_EVENT_TYPE_EVENT_TYPE_ID_fkey', 'EVENT_TYPE', ['EVENT_TYPE_ID'], ['ID'],
                                    ondelete='CASCADE')


def downgrade():
    with op.batch_alter_table('USER_ROLE') as batch_op:
        batch_op.drop_constraint('USER_ROLE_USER_ID_fkey', type_='foreignkey')
        batch_op.drop_constraint('USER_ROLE_ROLE_ID_fkey', type_='foreignkey')
        batch_op.create_foreign_key('USER_ROLE_USER_ID_fkey', 'USER', ['USER_ID'], ['ID'])
        batch_op.create_foreign_key('USER_ROLE_ROLE_ID_fkey', 'ROLE', ['ROLE_ID'], ['ID'])

    with op.batch_alter_table('ROLE_EVENT_TYPE') as batch_op:
        batch_op.drop_constraint('ROLE_EVENT_TYPE_ROLE_ID_fkey', type_='foreignkey')
        batch_op.drop_constraint('ROLE_EVENT_TYPE_EVENT_TYPE_ID_fkey', type_='foreignkey')
        batch_op.create_foreign_key('ROLE_EVENT_TYPE_ROLE_ID_fkey', 'ROLE', ['ROLE_ID'], ['ID'])
        batch_op.create_foreign_key('ROLE_EVENT_TYPE_EVENT_TYPE_ID_fkey', 'EVENT_TYPE', ['EVENT_TYPE_ID'], ['ID'])
