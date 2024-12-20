import graphene


class Query(graphene.ObjectType):
    hello_world = graphene.String(default='Hello World!')
