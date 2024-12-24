import graphene

from src.controllers.user_controller import UserController


class UserData(graphene.ObjectType):
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
    data = graphene.Field(UserData)

    @classmethod
    async def mutate(cls, root, info, name, last_name, username, email, mobile_phone, password):

        user_created = UserController().create_user(
            name=name, last_name=last_name, username=username, email=email,
            mobile_phone=mobile_phone, password=password,
        )

        return RegisterUser(result='User registered successfully.', data=UserData(id=user_created))


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
