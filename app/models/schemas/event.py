import datetime

from app.models.schemas.base import BaseSchemaModel


class EventInCreate(BaseSchemaModel):
    created_by: int
    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime


class EventInUpdate(BaseSchemaModel):
    title: str | None
    description: str | None
    start_date: datetime.datetime | None
    end_date: datetime.datetime | None


class EventInResponse(BaseSchemaModel):
    id: int
    created_by: int
    title: str
    description: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
