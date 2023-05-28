import datetime

from pydantic import BaseModel


class JWToken(BaseModel):
    exp: datetime.datetime
    sub: str


class JWTUser(BaseModel):
    username: str
