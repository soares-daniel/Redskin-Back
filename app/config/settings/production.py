from app.config.settings.base import BaseSettings
from app.config.settings.environment import Environment


class ProdSettings(BaseSettings):
    DESCRIPTION: str | None = "Production Environment."
    ENVIRONMENT: Environment = Environment.PRODUCTION
