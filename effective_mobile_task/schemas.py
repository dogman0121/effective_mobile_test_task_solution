from marshmallow import fields, Schema


class RegisterSchema(Schema):
    name = fields.String()
    last_name = fields.String()
    email = fields.String()
    password = fields.String()

class LoginSchema(Schema):
    email = fields.String()
    password = fields.String()

class UserUpdateSchema(Schema):
    name = fields.String()
    last_name = fields.String()
    email = fields.String()
    password = fields.String()

class UserSchema(Schema):
    name = fields.String()
    last_name = fields.String()
    email = fields.String()
    role = fields.Integer()

class PermissionCreateSchema(Schema):
    name = fields.String()
    role = fields.Integer()

class PermissionSchema(Schema):
    name = fields.String()
    role = fields.Integer()

class PermissionUpdateSchema(Schema):
    name = fields.String()
    role = fields.Integer()