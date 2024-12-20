from graphene import Schema
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from src.api.mutations import Mutation
from src.api.queries import Query

schema = Schema(query=Query, mutation=Mutation)


async def handler_graph(request):
    if request.method == 'POST':
        body = await request.json()
        query = body.get('query')
        variables = body.get('variables')

        response_query = await schema.execute_async(
            query, variables_values=variables,
        )

        result = {'data': response_query.data}

        return JSONResponse(result)

app = Starlette(
    debug=True,
    routes=[
        Route('/graphql', handler_graph, methods=['POST']),
    ],
)
