from pytest import mark

from src.models import User


@mark.asyncio
@mark.parametrize(
    'identifier_field, identifier_value', [
        ['username', 'username'],
        ['email', 'email'],
    ],
)
async def test_successful_login_with_valid_data(
        mock_prepare_db, client_api, default_user_record_constructor,
        identifier_field, identifier_value,
):
    mutation_login = '''
        mutation(
            $username: String,
            $email: String,
            $password: String!,
        ) {
            login(
                username: $username,
                email: $email,
                password: $password,
            ) {
                ok
                message
                user {
                    id
                }
            }
        }
    '''

    existing_user = await default_user_record_constructor

    mutation_variables = {
        identifier_field: getattr(existing_user, identifier_value),
        'password': existing_user.password,
    }
    response = client_api.post('/graphql', json={'query': mutation_login, 'variables': mutation_variables})
    response_data = response.json()

    result_login = response_data['login']
    assert result_login['ok'] is True
    assert result_login['message'] == 'Login successful.'
    assert result_login['user']['id'] is not None

    user_data = await User.get(id=result_login['user']['id'])
    assert getattr(user_data, identifier_value) == mutation_variables[identifier_field]


# TODO: tests,
"""
- Datos incorrectos.
- Password incorrecta con username correcto.
- Password incorrecta con email correcto.
- Password correcta con username incorrecto.
- Password correcta con email incorrecto.
- datos vacios.
- Datos nulos.
"""
