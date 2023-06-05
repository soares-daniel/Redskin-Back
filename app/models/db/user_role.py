from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class UserRole(Base):
    """Map roles to users."""
    __tablename__ = "USER_ROLE"

    user_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        foreign_key="USER.ID",
        nullable=False,
        name="USER_ID")
    role_id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        foreign_key="ROLE.ID",
        nullable=False,
        name="ROLE_ID")

    __mapper_args__ = {"eager_defaults": True}
