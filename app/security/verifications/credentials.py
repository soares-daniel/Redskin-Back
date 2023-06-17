import sqlalchemy


from app.database.database import async_db
from app.models.db.user import User


class CredentialVerifier:

    @staticmethod
    async def is_username_available(self, username: str | None) -> bool:
        # Assuming User is your SQLAlchemy model and session is your database session
        async with async_db.get_session() as async_session:
            check = await async_session.execute(sqlalchemy.select(User).filter(User.username == username))

            if username and check.scalar_one_or_none() is None:
                return True
            return False


def get_credential_verifier() -> CredentialVerifier:
    return CredentialVerifier()


credential_verifier: CredentialVerifier = get_credential_verifier()
