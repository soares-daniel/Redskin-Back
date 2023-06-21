import datetime

from app.models.schemas.base import BaseSchemaModel


class RoleInCreate(BaseSchemaModel):
    name: str


class RoleInUpdate(BaseSchemaModel):
    name: str | None


class RoleInResponse(BaseSchemaModel):
    name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
