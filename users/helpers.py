from users.models import User


def list_users():
    return User.objects.all()
