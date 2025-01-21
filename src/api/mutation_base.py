import graphene

from src.api.mutations.login_mutation import Login
from src.api.mutations.register_user_mutation import RegisterUser


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login = Login.Field()
