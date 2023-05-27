from app.config.settings.base import BaseSettings
from app.config.settings.environment import Environment


class DevSettings(BaseSettings):
    DESCRIPTION: str | None = "Development Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
