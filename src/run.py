from graphene import Schema
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route
from tortoise import Tortoise

from src.api.mutation_base import Mutation
from src.api.queries_base import Query
from src.env.base import API_PATH_NAME
from src.env.base import HOST_DATABASE_ARTEMIS
from src.env.base import NAME_DATABASE_ARTEMIS
from src.env.base import PASSWORD_DATABASE_ARTEMIS
from src.env.base import PORT_DATABASE_ARTEMIS
from src.env.base import USER_DATABASE_ARTEMIS


schema = Schema(query=Query, mutation=Mutation)


async def handler_graphql_request(request):
    if request.method == 'POST':
        body = await request.json()
        query = body.get('query')
        variables = body.get('variables')
        response_query = await schema.execute_async(query, variables=variables)

        if response_query.errors:
            return JSONResponse({'error': 'There was a problem with the fields provided. Please check the inputs.'})
        return JSONResponse({'data': response_query.data})


async def initialize_db():
    await Tortoise.init(
        db_url=f'postgres://{USER_DATABASE_ARTEMIS}:{PASSWORD_DATABASE_ARTEMIS}@{HOST_DATABASE_ARTEMIS}:'
        f'{PORT_DATABASE_ARTEMIS}/{NAME_DATABASE_ARTEMIS}',
        modules={'models': ['src.models']},
    )
    await Tortoise.generate_schemas(safe=True)


async def close_db():
    await Tortoise.close_connections()


app = Starlette(
    debug=True,
    on_startup=[initialize_db],
    routes=[Route(API_PATH_NAME, handler_graphql_request, methods=['POST'])],
    on_shutdown=[close_db],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # test front
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
