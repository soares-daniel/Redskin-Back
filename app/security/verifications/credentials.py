class CredentialVerifier:
    def is_username_available(self, username: str | None) -> bool:
        if username:
            return False
        return True

def get_credential_verifier() -> CredentialVerifier:
    return CredentialVerifier()


credential_verifier: CredentialVerifier = get_credential_verifier()
