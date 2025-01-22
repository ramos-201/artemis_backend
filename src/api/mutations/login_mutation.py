import graphene

from src.api.schemas.user_scheme import UserScheme


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
        return cls(
            ok=True,
            message='Login successful.',
            user=UserScheme(id='1'),
        )
