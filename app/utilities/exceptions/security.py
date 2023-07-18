class PasswordDoesNotMatch(Exception):
    """
    Throw an exception when the account password does not match the entity's hashed password from the database.
    """