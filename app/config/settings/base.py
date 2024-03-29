from typing import List, Tuple
import logging
import pathlib

import decouple
import pydantic

ROOT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.parent.parent.resolve()


class BaseSettings(pydantic.BaseSettings):
    TITLE: str = "LESPEAUXROUGES - API"
    DESCRIPTION: str = "API for LesPeauxRouges Dashboard"
    VERSION: str = "0.1.0"
    TIMEZONE: str = "Europe/Paris"
    DEBUG: bool = False

    # Server
    SERVER_HOST: str = decouple.config("SERVER_HOST", cast=str)
    SERVER_PORT: int = decouple.config("SERVER_PORT", cast=int)
    SERVER_WORKERS: int = decouple.config("SERVER_WORKERS", cast=int)
    API_PREFIX: str = "/api"
    DOCS_URL: str = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: str = "/redoc"
    OPENAPI_PREFIX: str = ""
    ASSETS_PATH: str = decouple.config("ASSETS_PATH", cast=str, default=str("../assets"))

    # Discord
    DISCORD_CLIENT_ID: str = decouple.config("DISCORD_CLIENT_ID", cast=str)  # type: ignore
    DISCORD_SERVER_PORT: int = decouple.config("DISCORD_SERVER_PORT", cast=int)  # type: ignore
    DISCORD_SERVER_HOST: str = decouple.config("DISCORD_SERVER_HOST", cast=str)  # type: ignore
    DISCORD_NOTIFICATION_ENDPOINT: str = decouple.config("DISCORD_NOTIFICATION_ENDPOINT", cast=str)  # type: ignore
    DISCORD_URL: str = f"http://{DISCORD_SERVER_HOST}:{DISCORD_SERVER_PORT}{DISCORD_NOTIFICATION_ENDPOINT}"

    # Frontend
    FRONTEND_HOST: str = decouple.config("FRONTEND_HOST", cast=str)  # type: ignore
    FRONTEND_PORT: int = decouple.config("FRONTEND_PORT", cast=int)  # type: ignore

    # Database
    DB_POSTGRES_NAME: str = decouple.config("POSTGRES_NAME", cast=str)
    DB_POSTGRES_HOST: str = decouple.config("POSTGRES_HOST", cast=str)
    DB_POSTGRES_PORT: int = decouple.config("POSTGRES_PORT", cast=int)
    DB_POSTGRES_USER: str = decouple.config("POSTGRES_USER", cast=str)
    DB_POSTGRES_PASSWORD: str = decouple.config("POSTGRES_PASSWORD", cast=str)
    DB_POSTGRES_SCHEMA: str = decouple.config("POSTGRES_SCHEMA", cast=str)
    DB_MAX_POOL_CON: int = decouple.config("DB_MAX_POOL_CON", cast=int)
    DB_POOL_SIZE: int = decouple.config("DB_POOL_SIZE", cast=int)
    DB_POOL_OVERFLOW: int = decouple.config("DB_POOL_OVERFLOW", cast=int)
    DB_TIMEOUT: int = decouple.config("DB_TIMEOUT", cast=int)

    IS_DB_ECHO_LOG: bool = decouple.config("IS_DB_ECHO_LOG", cast=bool)  # type: ignore
    IS_DB_FORCE_ROLLBACK: bool = decouple.config("IS_DB_FORCE_ROLLBACK", cast=bool)  # type: ignore
    IS_DB_EXPIRE_ON_COMMIT: bool = decouple.config("IS_DB_EXPIRE_ON_COMMIT", cast=bool)  # type: ignore

    # Security
    API_TOKEN: str = decouple.config("API_TOKEN", cast=str)  # type: ignore
    AUTH_TOKEN: str = decouple.config("AUTH_TOKEN", cast=str)  # type: ignore
    JWT_TOKEN_PREFIX: str = decouple.config("JWT_TOKEN_PREFIX", cast=str)  # type: ignore
    JWT_SECRET_KEY: str = decouple.config("JWT_SECRET_KEY", cast=str)  # type: ignore
    JWT_SUBJECT: str = decouple.config("JWT_SUBJECT", cast=str)  # type: ignore
    JWT_MIN: int = decouple.config("JWT_MIN", cast=int)  # type: ignore
    JWT_HOUR: int = decouple.config("JWT_HOUR", cast=int)  # type: ignore
    JWT_DAY: int = decouple.config("JWT_DAY", cast=int)  # type: ignore
    JWT_ACCESS_TOKEN_EXPIRATION_TIME: int = JWT_MIN * JWT_HOUR * JWT_DAY
    # TODO: ADD REFRESH TOKEN + IMPLEMENTATION

    IS_ALLOWED_CREDENTIALS: bool = decouple.config("IS_ALLOWED_CREDENTIALS", cast=bool)  # type: ignore
    ALLOWED_ORIGINS: List[str] = [
        f"http://localhost:{FRONTEND_PORT}",
        f"https://localhost:{FRONTEND_PORT}",
        f"http://localhost:{DISCORD_SERVER_PORT}",
        f"https://localhost:{DISCORD_SERVER_PORT}",
        f"http://{FRONTEND_HOST}:{FRONTEND_PORT}",
        f"https://{FRONTEND_HOST}:{FRONTEND_PORT}",
        f"http://{DISCORD_SERVER_HOST}:{DISCORD_SERVER_PORT}",
        f"https://{DISCORD_SERVER_HOST}:{DISCORD_SERVER_PORT}",
        f"http://http://ec2-3-127-231-16.eu-central-1.compute.amazonaws.com:{FRONTEND_PORT}",
        f"https://http://ec2-3-127-231-16.eu-central-1.compute.amazonaws.com:{FRONTEND_PORT}",
    ]
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]

    # Logging
    LOGGING_LEVEL: int = logging.INFO
    LOGGERS: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    LOGGING_FORMAT: str = "<green>{time:HH:mm:ss.SSSZ}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    # Hashing
    HASHING_ALGORITHM_LAYER_1: str = decouple.config("HASHING_ALGORITHM_LAYER_1", cast=str)  # type: ignore
    HASHING_ALGORITHM_LAYER_2: str = decouple.config("HASHING_ALGORITHM_LAYER_2", cast=str)  # type: ignore
    HASHING_SALT: str = decouple.config("HASHING_SALT", cast=str)  # type: ignore
    JWT_ALGORITHM: str = decouple.config("JWT_ALGORITHM", cast=str)  # type: ignore

    # Superuser
    SUPER_USER: str = decouple.config("SUPER_USER", cast=str)  # type: ignore
    SUPER_PASS: str = decouple.config("SUPER_PASS", cast=str)  # type: ignore

    class Config(pydantic.BaseConfig):
        case_sensitive: bool = True
        env_file: str = f"{str(ROOT_DIR)}/.env"
        validate_assignment: bool = True

    @property
    def set_app_attributes(self) -> dict[str, str | bool | None]:
        """Set all `FastAPI` class' attributes."""
        return {
            "title": self.TITLE,
            "version": self.VERSION,
            "debug": self.DEBUG,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
            "api_prefix": self.API_PREFIX,
        }
