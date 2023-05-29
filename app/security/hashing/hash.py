import secrets
import hashlib
import binascii
from app.config.manager import settings


class HashGenerator:
    def __init__(self):
        self._hash_ctx_salt: str = settings.HASHING_SALT

    @property
    def _get_hashing_salt(self) -> str:
        return self._hash_ctx_salt

    def generate_password_salt(self) -> str:
        """
        A function to generate a random salt.
        """
        # Generate a random salt
        return secrets.token_hex(16)

    def generate_password_hash(self, salt: str, password: str) -> str:
        """
        A function that adds the user's password with the salt, then hashes it using SHA512 algorithm.
        """
        if not salt or not password:
            raise ValueError("Invalid salt or password value.")
        dk = hashlib.pbkdf2_hmac('sha512', (salt + password).encode(), self._get_hashing_salt.encode(), 100000)
        return binascii.hexlify(dk).decode()

    def is_password_verified(self, salt: str, password: str, hashed_password: str) -> bool:
        """
        A function that verifies whether the password matches the hashed password.
        """
        if not password or not hashed_password:
            raise ValueError("Invalid password or hash.")
        return self.generate_password_hash(salt, password) == hashed_password


def get_hash_generator() -> HashGenerator:
    return HashGenerator()


hash_generator: HashGenerator = get_hash_generator()
