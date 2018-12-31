from marshmallow import Schema, fields, validate
from users.serializers import UserSchema


class TaskSchema(Schema):
    id = fields.Integer(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    description = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))
    due_date = fields.DateTime(required=False, allow_none=True)
