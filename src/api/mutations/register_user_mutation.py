import graphene

from src.api.schemas.user_scheme import UserScheme
from src.controllers.user_controller import UserController


class RegisterUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        mobile_phone = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserScheme)

    @classmethod
    async def mutate(
            cls,
            root,
            info,
            name: str,
            last_name: str,
            username: str,
            email: str,
            mobile_phone: str,
            password: str,
    ):
        user_controller = UserController()
        user_created, message = await user_controller.create_user(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
        )

        ok = bool(user_created)
        if ok and user_created:
            user = UserScheme(id=user_created.id)
        else:
            user = None

        return cls(
            ok=ok,
            message=message,
            user=user,
        )
