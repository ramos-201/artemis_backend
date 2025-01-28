from pytest import mark

from src.models import User
from tests.factory_test import UserFactory

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
    existing_user = await default_user_record_constructor

    mutation_variables = {
        identifier_field: getattr(existing_user, identifier_value),
        'password': existing_user.password,
    }
    response = client_api.post('/graphql', json={'query': mutation_login, 'variables': mutation_variables})
    response_data = response.json()

    result_login = response_data['login']
    assert result_login['ok'] is True
    assert result_login['message'] == 'User login was successful.'
    assert result_login['user']['id'] is not None

    user_data = await User.get(id=result_login['user']['id'])
    assert getattr(user_data, identifier_value) == mutation_variables[identifier_field]


valid_password = 'password_valid'
credentials_valid = 'credentials_valid@example.com'


@mark.asyncio
@mark.parametrize(
    'credentials_field_identifier, credentials_value, password_value', [
        ['username', 'username_invalid', valid_password],
        ['email', 'email_invalid', valid_password],
        ['username', credentials_valid, 'password_invalid'],
        ['email', credentials_valid, 'password_invalid'],
        ['username', 'credential_invalid', 'password_invalid'],
        ['email', 'credential_invalid', 'password_invalid'],
    ],
)
async def test_error_when_credentials_are_invalid(
        mock_prepare_db, client_api,
        credentials_field_identifier, credentials_value, password_value,
):
    existing_user = await UserFactory.build(
        password=valid_password,
        username=credentials_valid,
        email=credentials_valid,
    )
    await existing_user.save()

    mutation_variables = {
        credentials_field_identifier: credentials_value,
        'password': password_value,
    }
    response = client_api.post('/graphql', json={'query': mutation_login, 'variables': mutation_variables})
    response_data = response.json()

    result_login = response_data['login']
    assert result_login['ok'] is False
    assert result_login['message'] == 'The credentials entered are invalid.'
    assert result_login['user'] is None

# TODO: tests,
"""
- datos vacios.
- Datos nulos.
- No mutation_variables.
"""
