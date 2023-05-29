
# Generated by CodiumAI

# Dependencies:
# pip install pytest-mock
import datetime
import pytest

from jose import jwt as jose_jwt

from app.models.db.user import User
from app.security.authorization.jwt_generator import JWTGenerator
from app.config.manager import settings
from app.utilities.exceptions.database import EntityDoesNotExist

"""
Code Analysis

Main functionalities:
The JWTGenerator class is responsible for generating and retrieving details from JSON Web Tokens (JWTs). It has two main functionalities: generating an access token for a given user and retrieving the username from a given token. It uses the Pydantic library to define the JWTUser and JWToken models, and the jose library to encode and decode the tokens. It also uses the EntityDoesNotExist exception from the app.utilities.exceptions.database module to raise an error if the user entity is not provided when generating a token.

Methods:
- _generate_jwt_token: a private method that takes in a dictionary of JWT data and an optional expiration time, and returns a JWT token encoded with the provided secret key and algorithm.
- generate_access_token: a public method that takes in a User object and returns an access token for that user, using the _generate_jwt_token method.
- retrieve_details_from_token: a static method that takes in a JWT token and a secret key, decodes the token, validates its payload, and returns the username from the token.

Fields:
- None.
"""


class TestJWTGenerator:

    #  Tests that generate_access_token method returns a valid JWT token for a given User entity.
    def test_generate_access_token_valid_user(self, mocker):
        user = User(username="test_user")
        jwt_generator = JWTGenerator()
        mocker.patch.object(jwt_generator, "_generate_jwt_token", return_value="valid_token")

        token = jwt_generator.generate_access_token(user)

        assert token == "valid_token"

    #  Tests that retrieve_details_from_token method successfully decodes and validates a valid JWT token.
    def test_retrieve_details_from_token_valid_token(self, mocker):
        jwt_data = {"username": "test_user"}
        token = jose_jwt.encode(jwt_data, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        jwt_generator = JWTGenerator()

        details = jwt_generator.retrieve_details_from_token(token, settings.JWT_SECRET_KEY)

        assert details == ["test_user"]

    #  Tests that generate_access_token method raises EntityDoesNotExist exception when given a None user.
    def test_generate_access_token_none_user(self):
        jwt_generator = JWTGenerator()

        with pytest.raises(EntityDoesNotExist):
            jwt_generator.generate_access_token(None)

    #  Tests that retrieve_details_from_token method raises ValueError when given an invalid JWT token.
    def test_retrieve_details_from_token_invalid_token(self):
        jwt_generator = JWTGenerator()

        with pytest.raises(ValueError):
            jwt_generator.retrieve_details_from_token("invalid_token", settings.JWT_SECRET_KEY)

    #  Tests that retrieve_details_from_token method raises ValueError when given a revoked JWT token.
    def test_retrieve_details_from_token_revoked_token(self, mocker):
        jwt_data = {"username": "test_user"}
        token = jose_jwt.encode(jwt_data, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        jwt_generator = JWTGenerator()
        mocker.patch.object(jwt_generator, "retrieve_details_from_token", side_effect=ValueError("Token has been revoked"))

        with pytest.raises(ValueError):
            jwt_generator.retrieve_details_from_token(token, settings.JWT_SECRET_KEY)

    #  Tests that retrieve_details_from_token method raises ValueError when given an expired JWT token.
    def test_retrieve_details_from_token_expired_token(self, mocker):
        jwt_data = {"username": "test_user", "exp": datetime.datetime.utcnow() - datetime.timedelta(minutes=1)}
        token = jose_jwt.encode(jwt_data, key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        jwt_generator = JWTGenerator()

        with pytest.raises(ValueError):
            jwt_generator.retrieve_details_from_token(token, settings.JWT_SECRET_KEY)
