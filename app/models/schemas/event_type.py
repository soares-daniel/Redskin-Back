from app.models.schemas.base import BaseSchemaModel


class EventTypeInCreate(BaseSchemaModel):
    name: str
    description: str


class EventTypeInUpdate(BaseSchemaModel):
    name: str
    description: str


class EventTypeInResponse(BaseSchemaModel):
    name: str
    description: str
