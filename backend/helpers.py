from rest_framework_jwt.utils import jwt_payload_handler as default_jwt_payload_handler


def jwt_payload_handler(user):
    payload = default_jwt_payload_handler(user)
    payload.update({
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
    })
    return payload
