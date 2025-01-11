from tortoise import fields
from tortoise import Model


class User(Model):
    id = fields.IntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    username = fields.CharField(unique=True, max_length=100)
    email = fields.CharField(unique=True, max_length=100)
    mobile_phone = fields.CharField(unique=True, max_length=20)
    password = fields.CharField(max_length=100)
    is_active_account = fields.BooleanField(default=False)
    date_account_activated = fields.DateField(null=True)
