import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class RoleEventType(Base):
    """Role event type table."""
    __tablename__ = "ROLE_EVENT_TYPE"

    role_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        ForeignKey("ROLE.ID"),
        primary_key=True,
        name="ROLE_ID")
    event_type_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        ForeignKey("EVENT_TYPE.ID"),
        primary_key=True,
        name="EVENT_TYPE_ID")
    can_edit: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean,
        default=False,
        name="CAN_EDIT")
    can_see: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean,
        default=False,
        name="CAN_SEE")
    can_add: SQLAlchemyMapped[bool] = sqlalchemy_mapped_column(
        sqlalchemy.Boolean,
        default=False,
        name="CAN_ADD")

    role = relationship("Role")
    event_type = relationship("EventType")
