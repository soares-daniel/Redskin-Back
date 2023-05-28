from functools import lru_cache

import decouple

from app.config.settings.base import BaseSettings
from app.config.settings.development import DevSettings
from app.config.settings.environment import Environment
from app.config.settings.production import ProdSettings
from app.config.settings.testing import TestSettings


class SettingsFactory:
    def __init__(self, environment: str):
        self.environment = environment

    def __call__(self) -> BaseSettings:
        if self.environment == Environment.DEVELOPMENT.value:
            return DevSettings()
        elif self.environment == Environment.TESTING.value:
            return TestSettings()
        return ProdSettings()


@lru_cache()
def get_settings() -> BaseSettings:
    return SettingsFactory(environment=decouple.config("ENVIRONMENT", default="DEV", cast=str))()  # type: ignore


settings: BaseSettings = get_settings()
