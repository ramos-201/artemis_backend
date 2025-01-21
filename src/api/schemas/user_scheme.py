import graphene


class UserScheme(graphene.ObjectType):
    id = graphene.String()
