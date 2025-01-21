import graphene

from src.api.schemas.user_scheme import UserScheme
# from src.controllers.user_controller import UserController


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=False)
        email = graphene.String(required=False)
        password = graphene.String(required=True)

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
        return cls(
            ok=True,
            message='Login successful.',
            user=UserScheme(id='1'),
        )
