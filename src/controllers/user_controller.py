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
        user_created = await self.__model.create(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
        )

        return user_created
