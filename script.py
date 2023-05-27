import requests
import random
import string

BASE_URL = "http://localhost:8000"


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))


def create_user(username, password):
    url = f"{BASE_URL}/users/"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print(f"User created: username={username}, password={password}")
    else:
        print(f"Failed to create user: {response.text}")


# Number of users to create
num_users = 30

for _ in range(num_users):
    username = generate_random_string(8)
    password = generate_random_password(12)
    create_user(username, password)