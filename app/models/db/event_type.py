import sqlalchemy
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

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

    # role_event_types = sqlalchemy_relationship("RoleEventType", back_populates="event_type")

    __mapper_args__ = {"eager_defaults": True}
