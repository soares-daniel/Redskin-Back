def http_400_username_details(username: str) -> str:
    return f"The username {username} is taken! Be creative and choose another one!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed! Recheck all your credentials!"


def http_400_signin_credentials_details() -> str:
    return "Signin failed! Recheck all your credentials!"


def http_400_email_details(email: str) -> str:
    return f"The email {email} is already registered! Be creative and choose another one!"


def http_401_unauthorized_details() -> str:
    return "Refused to complete request due to lack of valid authentication!"


def http_403_forbidden_details() -> str:
    return "Refused access to the requested resource!"


def http_403_permission_denied_details() -> str:
    return "Not enough permissions to perform this operation!"


def http_403_missing_role() -> str:
    return "Missing required role to access this resource!"


def http_404_id_details(_object: str, _id: int) -> str:
    return f"Either the {_object} with id `{_id}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_username_details(username: str) -> str:
    return f"Either the user with username `{username}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_email_details(email: str) -> str:
    return f"Either the user with email `{email}` doesn't exist, has been deleted, or you are not authorized!"


def http_404_user_role_details(user_id: int, role_id: int) -> str:
    return f"User with id {user_id} or Role with id {role_id} does not exist!"


def http_404_user_role_relation_details(user_id: int, role_id: int) -> str:
    return f"User with id {user_id} does not have a role with id {role_id}"
