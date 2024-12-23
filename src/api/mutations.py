import graphene


class RegisterUser(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        mobile_phone = graphene.String(required=True)
        password = graphene.String(required=True)

    result = graphene.String()

    @classmethod
    async def mutate(cls, root, info, name, last_name, username, email, mobile_phone, password):
        return RegisterUser(result='User registered successfully.')


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
