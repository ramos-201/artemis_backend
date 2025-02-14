from typing import Optional

from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from src.exceptions import DuplicateFieldError
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
    ) -> 'User':
        try:
            return await self.__model.create(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except IntegrityError as error:
            field_name = str(error).split()[-1].split('.')[-1]
            raise DuplicateFieldError(f'The data for the field "{field_name}" already exists.')

    async def get_user_with_credentials(
            self,
            password: str,
            username: Optional[str] = None,
            email: Optional[str] = None,
    ) -> Optional['User']:
        return await self.__model.get_or_none(
            (Q(username=username) | Q(email=email)),
            password=password,
        )
