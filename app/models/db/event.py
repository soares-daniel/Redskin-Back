import datetime

import sqlalchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped as SQLAlchemyMapped, mapped_column as sqlalchemy_mapped_column

from app.database.table import Base


class Event(Base):
    """Event table."""
    __tablename__ = "EVENT"

    id: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        primary_key=True,
        autoincrement=True,
        name="ID")
    created_by: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        ForeignKey("USER.ID"),
        nullable=False,
        name="CREATED_BY")
    event_type: SQLAlchemyMapped[int] = sqlalchemy_mapped_column(
        ForeignKey("EVENT_TYPE.ID"),
        nullable=False,
        name="EVENT_TYPE")
    title: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=False,
        name="TITLE")
    description: SQLAlchemyMapped[str] = sqlalchemy_mapped_column(
        sqlalchemy.String(length=1024),
        nullable=True,
        name="DESCRIPTION")
    start_date: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        name="START_DATE")
    end_date: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=False,
        name="END_DATE")
    created_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        name="CREATED_AT")
    updated_at: SQLAlchemyMapped[datetime.datetime] = sqlalchemy_mapped_column(
        sqlalchemy.DateTime(timezone=True),
        nullable=True,
        server_onupdate=sqlalchemy.schema.FetchedValue(for_update=True),
        name="UPDATED_AT")

    __mapper_args__ = {"eager_defaults": True}
