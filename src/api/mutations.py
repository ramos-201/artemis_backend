import graphene

from src.controllers.user_controller import UserController
from src.exceptions.exceptions import EmptyFieldError


class UserScheme(graphene.ObjectType):
    id = graphene.String()


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
            name,
            last_name,
            username,
            email,
            mobile_phone,
            password,
    ):
        user_controller = UserController()

        try:
            user_created, message = await user_controller.create_user(
                name=name,
                last_name=last_name,
                username=username,
                email=email,
                mobile_phone=mobile_phone,
                password=password,
            )
        except EmptyFieldError as e:
            user_created = None
            message = str(e)

        ok = False
        user = None

        if user_created:
            ok = True
            user = UserScheme(id=user_created.id)

        return cls(
            ok=ok,
            message=message,
            user=user,
        )


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
