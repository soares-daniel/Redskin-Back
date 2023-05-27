from datetime import datetime

from app.models.schemas.base import BaseSchemaModel


class UserInCreate(BaseSchemaModel):
    username: str
    password: str


class UserInUpdate(BaseSchemaModel):
    username: str | None
    password: str | None


class UserInLogin(BaseSchemaModel):
    username: str
    password: str


class UserWithToken(BaseSchemaModel):
    token: str
    username: str
    created_at: datetime
    updated_at: datetime | None


class UserInResponse(BaseSchemaModel):
    id: int
    authorized_user: UserWithToken
