import sqlalchemy
from sqlalchemy.orm import (relationship as sqlalchemy_relationship,
                            Mapped as SQLAlchemyMapped,
                            mapped_column as sqlalchemy_mapped_column)

from app.database.table import Base


class EventType(Base):
    """Event type table."""
    __tablename__ = "EVENT_TYPE"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True,
        autoincrement=True,
        name="ID")
    name: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=False,
        name="NAME")
    description: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=True,
        name="DESCRIPTION")

    roles = sqlalchemy_relationship("Role", secondary="ROLE_EVENT_TYPE", back_populates="event_types")

    __mapper_args__ = {"eager_defaults": True}
