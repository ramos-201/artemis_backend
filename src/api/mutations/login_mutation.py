import graphene

from src.api.schemas.user_scheme import UserScheme
from src.controllers.user_controller import UserController


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
        user_controller = UserController()

        existing_user = await user_controller.get_user_with_credentials(
            password=password,
            username=username,
            email=email,
        )

        if existing_user:
            return cls(
                ok=True,
                message='User login was successful.',
                user=UserScheme(id=existing_user.id),
            )

        return cls(
            ok=False,
            message='The credentials entered are invalid.',
            user=None,
        )
