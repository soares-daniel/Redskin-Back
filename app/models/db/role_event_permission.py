from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class RoleEventPermission(Base):
    """Maps roles to event types and permissions."""
    __tablename__ = "ROLE_EVENT_PERMISSION"

    role_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        foreign_key="ROLE.ID",
        nullable=False,
        name="ROLE_ID")
    event_type_id: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        foreign_key="EVENT_TYPE.ID",
        nullable=False,
        name="EVENT_TYPE_ID")
    permission_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        foreign_key="PERMISSION.ID",
        nullable=False,
        name="PERMISSION_ID")

    __mapper_args__ = {"eager_defaults": True}
