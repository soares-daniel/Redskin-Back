"""fix start_date and end_date from event

Revision ID: d0a2e9f40e01
Revises: 66f84a686e68
Create Date: 2023-06-29 19:40:32.750623

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0a2e9f40e01'
down_revision = '66f84a686e68'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    ALTER TABLE "EVENT"
    ALTER COLUMN "START_DATE" TYPE TIMESTAMP WITH TIME ZONE 
    USING "START_DATE"::timestamp with time zone
    """)
    op.execute("""
    ALTER TABLE "EVENT"
    ALTER COLUMN "END_DATE" TYPE TIMESTAMP WITH TIME ZONE 
    USING "END_DATE"::timestamp with time zone
    """)


def downgrade():
    op.alter_column('EVENT', 'START_DATE',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.VARCHAR(length=1024),
                    existing_nullable=False)
    op.alter_column('EVENT', 'END_DATE',
                    existing_type=sa.DateTime(timezone=True),
                    type_=sa.VARCHAR(length=1024),
                    existing_nullable=False)
    # ### end Alembic commands ###
