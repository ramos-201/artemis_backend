from typing import Optional

from tortoise.exceptions import IntegrityError

from src.exceptions.exceptions import EmptyFieldError
from src.models import User


def validate_non_empty_fields(**value):
    for key, value in value.items():
        if not value or not value.strip():
            raise EmptyFieldError(f'The field "{key}" cannot be empty or contain only spaces.')


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
            validate_non_empty_fields(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except EmptyFieldError as e:
            return None, str(e)

        try:
            user_created = await self.__model.create(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except IntegrityError as e:
            field_name = str(e).split()[-1].split('.')[-1]
            return None, f'Error: {field_name} data already exists'

        return user_created, 'User registered successfully.'
