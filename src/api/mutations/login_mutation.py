import graphene

from src.api.schemas.user_scheme import UserScheme
from src.controllers.user_controller import UserController


def is_field_null_or_empty(field) -> bool:
    return not (str(field or '').strip())


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
            password,
            username=None,
            email=None,
    ):
        if (is_field_null_or_empty(username) and is_field_null_or_empty(email)) or is_field_null_or_empty(password):
            return cls(
                ok=False,
                message='Required fields cannot be null or empty.',
                user=None,
            )

        ok = False
        message = 'The fields cannot be empty or contain only spaces.'
        user = None
        if email or username:
            user_controller = UserController()
            existing_user = await user_controller.get_user_with_credentials(
                password=password,
                username=username,
                email=email,
            )

            message = 'The credentials entered are invalid.'
            if existing_user:
                ok = True
                message = 'User login was successful.'
                user = UserScheme(id=existing_user.id)

        return cls(
            ok=ok,
            message=message,
            user=user,
        )
