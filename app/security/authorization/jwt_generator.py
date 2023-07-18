import datetime

import pydantic
from jose import jwt as jose_jwt, JWTError as JoseJWTError
from loguru import logger

from app.config.manager import settings
from app.models.db.user import User
from app.models.schemas.jwt import JWTUser, JWToken
from app.utilities.exceptions.database import EntityDoesNotExist


class JWTGenerator:
    def __init__(self):
        self.logger = logger.bind(name="debug")

    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: datetime.timedelta | None = None,
    ) -> str:
        self.logger.debug(f"Generating JWT token")

        to_encode = jwt_data.copy()
        if expires_delta:
            expire = datetime.datetime.utcnow() + expires_delta
        else:
            expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.JWT_MIN)
        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())

        self.logger.debug(f"JWT token generated successfully")

        return jose_jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def generate_access_token(self, user: User) -> str:
        if not user:
            raise EntityDoesNotExist(f"Cannot generate JWT token without User entity!")

        self.logger.debug(f"Generating JWT access token for user: {user.username}")

        return self._generate_jwt_token(
            jwt_data=JWTUser(username=user.username).dict(),  # type: ignore
            expires_delta=datetime.timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME),
        )

    def retrieve_details_from_token(self, token: str) -> list[str]:
        self.logger.debug(f"Retrieving details from JWT token")
        try:
            payload = jose_jwt.decode(token=token, key=settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            jwt_user = JWTUser(username=payload["username"])

        except JoseJWTError as token_decode_error:
            raise ValueError("Unable to decode JWT Token") from token_decode_error
        except pydantic.ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        self.logger.debug(f"Details retrieved successfully from JWT token")

        return [jwt_user.username]


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
