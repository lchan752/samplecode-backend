from users.models import User


def is_email_already_used(email: str):
    return User.objects.filter(email=email).exists()


def list_users():
    return User.objects.all()


def create_user(first_name: str, last_name: str, email: str, password: str) -> User:
    user = User.objects.create_user(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    return user
