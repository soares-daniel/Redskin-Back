import sqlalchemy
from sqlalchemy.orm import (relationship as sqlalchemy_relationship,
                            Mapped as SQLAlchemyMapped,
                            mapped_column as sqlalchemy_mapped_column)

from app.database.table import Base
from app.models.db.user_role import user_roles


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

    users = sqlalchemy_relationship("User", secondary=user_roles, back_populates="roles")
    event_types = sqlalchemy_relationship("EventType", secondary="ROLE_EVENT_TYPE", back_populates="roles")

    __mapper_args__ = {"eager_defaults": True}
