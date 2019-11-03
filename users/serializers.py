from marshmallow import Schema, fields, validate, ValidationError
from users.helpers import is_email_already_used


def validate_email_unique(email: str):
    if is_email_already_used(email):
        raise ValidationError("Email already used")


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True, allow_none=False, validate=[validate.Email(), validate_email_unique])
    first_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))
    last_name = fields.String(required=True, allow_none=False, validate=validate.Length(min=1))
    password = fields.String(load_only=True, required=True, allow_none=False, validate=validate.Length(min=1))
    date_joined = fields.DateTime(dump_only=True)
    is_staff = fields.Boolean(dump_only=True)
