from datetime import datetime, timedelta

from pydantic import ValidationError
from jose import jwt as jose_jwt, JWTError as JoseJWTError

from app.config.manager import settings
from app.models.db.user import User
from app.models.schemas.jwt import JWTUser, JWToken
from app.utilities.exceptions.database import EntityDoesNotExist


class JWTGenerator:
    def __init__(self):
        pass

    @staticmethod
    def _generate_jwt_token(
        self,
        *,
        jwt_data: dict[str, str],
        expires_delta: timedelta | None = None,
    ) -> str:
        to_encode = jwt_data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_MIN)
        to_encode.update(JWToken(exp=expire, sub=settings.JWT_SUBJECT).dict())

        return jose_jwt.encode(to_encode, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    def generate_access_token(self, user: User) -> str:
        if not user:
            raise EntityDoesNotExist(f"Cannot generate JWT token without User entity!")

        return self._generate_jwt_token(
            jwt_data=JWTUser(username=user.username).dict(),  # type: ignore
            expires_delta=timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRATION_TIME),
        )

    @staticmethod
    def retrieve_details_from_token(self, token: str, secret_key: str) -> list[str]:
        try:
            payload = jose_jwt.decode(token=token, key=secret_key, algorithms=[settings.JWT_ALGORITHM])
            jwt_user = JWTUser(username=payload["username"])

        except JoseJWTError as token_decode_error:
            raise ValueError("Unable to decode JWT Token") from token_decode_error
        except ValidationError as validation_error:
            raise ValueError("Invalid payload in token") from validation_error

        return [jwt_user.username]


def get_jwt_generator() -> JWTGenerator:
    return JWTGenerator()


jwt_generator: JWTGenerator = get_jwt_generator()
