users = [
    {"id": 1, "username": "admin_bwi", "email": "admin@stikom.ac.id", "role": "admin"}
]


def get_all_users():
    return users


def add_user(username, email, role):
    user = {
        "id": max((existing["id"] for existing in users), default=0) + 1,
        "username": username,
        "email": email,
        "role": role
    }
    users.append(user)
    return user