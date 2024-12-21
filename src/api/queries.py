import graphene


class Query(graphene.ObjectType):
    hello_world = graphene.String(default_value='Hello World!')
