from sqlalchemy import ForeignKey, Table, Column

from app.database.table import Base

user_roles = Table(
    "USER_ROLE",
    Base.metadata,
    Column("USER_ID", ForeignKey("USER.ID", ondelete="CASCADE"), primary_key=True),
    Column("ROLE_ID", ForeignKey("ROLE.ID", ondelete="CASCADE"), primary_key=True)
)
