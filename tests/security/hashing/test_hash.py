import pytest

from app.security.hashing.hash import HashGenerator


class TestHashGenerator:
    def test_generate_password_hash_and_verification(self):
        hash_gen = HashGenerator()
        salt = hash_gen.generate_password_salt()
        password = "password"
        hashed_password = hash_gen.generate_password_hash(salt, password)

        assert hash_gen.is_password_verified(salt, password, hashed_password) == True

    def test_is_password_verified_with_incorrect_password(self):
        hash_gen = HashGenerator()
        salt = hash_gen.generate_password_salt()
        password = "password"
        hashed_password = hash_gen.generate_password_hash(salt, password)

        assert hash_gen.is_password_verified(salt, "wrong_password", hashed_password) == False
