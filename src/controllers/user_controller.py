from typing import Optional

from tortoise.exceptions import IntegrityError

from src.models import User


def validate_string_is_not_empty(value: str, field_description: str):
    if not value or not value.strip():
        raise ValueError(f'The field "{field_description}" cannot be empty or contain only spaces.')
    return value


class UserController:

    def __init__(self):
        self.__model = User

    async def create_user(
            self,
            name: str,
            last_name: str,
            username: str,
            email: str,
            mobile_phone: str,
            password: str,
    ) -> tuple[Optional['User'], str]:
        try:
            user_created = await self.__model.create(
                name=validate_string_is_not_empty(name, 'name'),
                last_name=validate_string_is_not_empty(last_name, 'last_name'),
                username=validate_string_is_not_empty(username, 'username'),
                email=validate_string_is_not_empty(email, 'email'),
                mobile_phone=validate_string_is_not_empty(mobile_phone, 'mobile_phone'),
                password=validate_string_is_not_empty(password, 'password'),
            )
        except IntegrityError as e:
            field_name = str(e).split()[-1].split('.')[-1]
            return None, f'Error: {field_name} data already exists'

        return user_created, 'User registered successfully.'
