# Generated by CodiumAI

import pytest
import pydantic

from app.config.manager import SettingsFactory, get_settings
from app.config.settings.production import ProdSettings

"""
Code Analysis

Main functionalities:
The SettingsFactory class is responsible for creating an instance of the appropriate settings class based on the environment variable. 
It takes in an environment string and returns an instance of the corresponding settings class, which inherits from the BaseSettings class. 
This allows for easy configuration of the application's settings based on the environment it is running in.

Methods:
- __init__(self, environment: str): Initializes the SettingsFactory object with the given environment string.
- __call__(self) -> BaseSettings: Returns an instance of the appropriate settings class based on the environment string.

Fields:
- environment: A string representing the environment the application is running in.
"""


class TestSettingsFactory:
    #  Tests that a SettingsFactory object can be created with a valid environment string.
    def test_create_settings_factory_object_with_valid_environment(self):
        # Happy path test for creating a SettingsFactory object with a valid environment string
        environment = "DEV"
        settings_factory = SettingsFactory(environment)
        assert settings_factory.environment == environment

    #  Tests that a SettingsFactory object cannot be created with an invalid environment string.
    def test_create_settings_factory_object_with_invalid_environment(self):
        # Edge case test for creating a SettingsFactory object with an invalid environment string
        environment = "INVALID"
        with pytest.raises(ValueError) as exc_info:
            SettingsFactory(environment)

    #  Tests that the function returns a valid instance of BaseSettings when called with a valid environment value.
    def test_get_settings_returns_valid_instance(self, monkeypatch):
        monkeypatch.setenv("ENVIRONMENT", "DEVELOPMENT")
        settings = get_settings()
        assert isinstance(settings, pydantic.BaseSettings)
