import datetime

from app.models.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    username: str
    first_name: str | None
    last_name: str | None
    password: str


class UserInUpdate(BaseSchemaModel):
    username: str | None
    first_name: str | None
    last_name: str | None
    profile_pic_url: str | None


class UserInLogin(BaseSchemaModel):
    username: str
    password: str


class UserInResponse(BaseSchemaModel):
    id: int
    username: str
    first_name: str | None
    last_name: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime | None
    profile_pic_url: str | None
