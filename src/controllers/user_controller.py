from typing import Optional

from tortoise.exceptions import IntegrityError

from src.models import User


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
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )

            return user_created, 'User registered successfully.'
        except IntegrityError as e:
            field_name = str(e).split()[-1].split('.')[-1]
            return None, f'Error: {field_name} data already exists'
