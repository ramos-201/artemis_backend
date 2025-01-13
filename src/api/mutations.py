import graphene

from src.controllers.user_controller import UserController


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

    result = graphene.String()
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
        user_created = await user_controller.create_user(
            name=name,
            last_name=last_name,
            username=username,
            email=email,
            mobile_phone=mobile_phone,
            password=password,
        )

        return RegisterUser(
            result='User registered successfully.',
            user=UserScheme(id=user_created.id),
        )


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
