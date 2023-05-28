from app.security.hashing.hash import hash_generator


class PasswordGenerator:
    @property
    def generate_salt(self) -> str:
        return hash_generator.generate_password_salt_hash

    @staticmethod
    def generate_hashed_password(hash_salt: str, new_password: str) -> str:
        return hash_generator.generate_password_hash(hash_salt=hash_salt, password=new_password)

    @staticmethod
    def is_password_authenticated(hash_salt: str, password: str, hashed_password: str) -> bool:
        return hash_generator.is_password_verified(password=hash_salt + password, hashed_password=hashed_password)


def get_pwd_generator() -> PasswordGenerator:
    return PasswordGenerator()


pass_generator: PasswordGenerator = get_pwd_generator()
