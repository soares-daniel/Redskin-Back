import pytest
from unittest.mock import AsyncMock, patch
from app.security.verifications.credentials import credential_verifier
from app.database.database import async_db
from app.models.db.user import User


class TestCredentialVerifier:
    pass