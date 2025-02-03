from typing import Optional

import graphene

from src.api.schemas.user_scheme import UserScheme
from src.controllers.user_controller import UserController
from src.utils import is_field_null_or_empty


class Login(graphene.Mutation):
    class Arguments:
        password = graphene.String(required=True)
        username = graphene.String(required=False)
        email = graphene.String(required=False)

    ok = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserScheme)

    @classmethod
    async def mutate(
            cls,
            root,
            info,
            password: str,
            username: Optional[str] = None,
            email: Optional[str] = None,
    ):
        if (
            is_field_null_or_empty(password) or
            (
                is_field_null_or_empty(email) and
                is_field_null_or_empty(username)
            )
        ):
            return cls(
                ok=False,
                message='Required fields cannot be null or empty.',
                user=None,
            )

        user_controller = UserController()
        existing_user = await user_controller.get_user_with_credentials(
            password=password,
            username=username,
            email=email,
        )

        if not existing_user:
            return cls(
                ok=False,
                message='The credentials entered are invalid.',
                user=None,
            )

        return cls(
            ok=True,
            message='User login was successful.',
            user=UserScheme(id=existing_user.id),
        )
