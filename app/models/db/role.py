import sqlalchemy
from sqlalchemy.orm import relationship as sqlalchemy_relationship, Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class Role(Base):
    """Role table."""
    __tablename__ = "ROLE"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True,
        autoincrement=True,
        name="ID")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=False,
        name="NAME")

    users = sqlalchemy_relationship("User", secondary="USER_ROLE", backref="ROLE")
    event_types = sqlalchemy_relationship("EventType", secondary="ROLE_EVENT_TYPE", backref="ROLE")

    __mapper_args__ = {"eager_defaults": True}
