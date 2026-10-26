from app.repositories import user_repo


def get_users():
    return user_repo.get_all_users()


def register_user(username, email, role):
    return user_repo.add_user(username, email, role)