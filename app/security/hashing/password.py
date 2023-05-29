from app.security.hashing.hash import hash_generator


class PasswordGenerator:
    @property
    def generate_salt(self) -> str:
        return hash_generator.generate_password_salt()

    @staticmethod
    def generate_hashed_password(salt: str, password: str) -> str:
        return hash_generator.generate_password_hash(salt=salt, password=password)

    @staticmethod
    def is_password_authenticated(salt: str, password: str, hashed_password: str) -> bool:
        return hash_generator.is_password_verified(salt=salt, password=password, hashed_password=hashed_password)


def get_pwd_generator() -> PasswordGenerator:
    return PasswordGenerator()


pass_generator: PasswordGenerator = get_pwd_generator()
