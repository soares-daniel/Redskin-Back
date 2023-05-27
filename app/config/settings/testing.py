from app.config.settings.base import BaseSettings
from app.config.settings.environment import Environment


class TestSettings(BaseSettings):
    DESCRIPTION: str | None = "Test Environment."
    DEBUG: bool = True
    ENVIRONMENT: Environment = Environment.TESTING
