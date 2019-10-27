from rest_framework_jwt.utils import jwt_payload_handler as default_jwt_payload_handler
from users.serializers import UserSchema


def jwt_payload_handler(user):
    payload = default_jwt_payload_handler(user)
    ser = UserSchema()
    payload.update(ser.dump(user).data)
    return payload
