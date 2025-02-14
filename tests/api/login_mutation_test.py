from pytest import mark

from src.env.base import API_PATH_NAME
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
           codeError
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
async def test_login_user_success(
        mock_prepare_db, client_api, default_user_record_constructor,
        identifier_field, identifier_value,
):
    existing_user = await default_user_record_constructor

    mutation_variables = {
        identifier_field: getattr(existing_user, identifier_value),
        'password': existing_user.password,
    }
    response = client_api.post(API_PATH_NAME, json={'query': mutation_login, 'variables': mutation_variables})
    response_json = response.json()

    assert response_json == {
        'data': {
            'login': {
                'ok': True,
                'codeError': None,
                'message': 'User login was successful.',
                'user': {'id': str(existing_user.id)},
            },
        },
    }

    user_data = await User.get(id=response_json['data']['login']['user']['id'])
    assert getattr(user_data, identifier_value) == mutation_variables[identifier_field]


@mark.asyncio
@mark.parametrize(
    'credentials_field_identifier, credentials_value, password_value', [
        ['username', 'username_invalid', 'password_valid'],
        ['email', 'email_invalid@example.com', 'password_valid'],
        ['username', 'username_valid', 'password_invalid'],
        ['email', 'email_valid@example.com', 'password_invalid'],
        ['username', 'username_invalid', 'password_invalid'],
        ['email', 'email_invalid@example.com', 'password_invalid'],
    ],
)
async def test_error_when_credentials_are_invalid(
        mock_prepare_db, client_api,
        credentials_field_identifier, credentials_value, password_value,
):
    existing_user = await UserFactory.build(
        password='password_valid',
        username='username_valid',
        email='email_valid@example.com',
    )
    await existing_user.save()

    mutation_variables = {
        credentials_field_identifier: credentials_value,
        'password': password_value,
    }
    response = client_api.post(API_PATH_NAME, json={'query': mutation_login, 'variables': mutation_variables})

    assert response.json() == {
        'data': {
            'login': {
                'ok': False,
                'codeError': 101,
                'message': 'The credentials entered are invalid.',
                'user': None,
            },
        },
    }


@mark.asyncio
@mark.parametrize(
    'mutation_variables', [
        {'username': '', 'password': 'pass_example'},
        {'email': '', 'password': 'pass_example'},
        {'username': 'john.smit', 'password': ''},
        {'email': 'john.smit@example.com', 'password': ''},
        {'username': None, 'password': 'pass_example'},
        {'email': None, 'password': 'pass_example'},
    ],
)
async def test_error_when_credentials_are_empty_or_null(mock_prepare_db, client_api, mutation_variables):
    response = client_api.post(API_PATH_NAME, json={'query': mutation_login, 'variables': mutation_variables})
    assert response.json() == {
        'data': {
            'login': {
                'ok': False,
                'codeError': 100,
                'message': 'Required fields cannot be null or empty.',
                'user': None,
            },
        },
    }


@mark.asyncio
@mark.parametrize(
    'mutation_variables', [
        {'password': None},
        None,
    ],
)
async def test_error_when_required_variables_are_sent_null(mock_prepare_db, client_api, mutation_variables):
    response = client_api.post(API_PATH_NAME, json={'query': mutation_login, 'variables': mutation_variables})
    assert response.json() == {'error': 'There was a problem with the fields provided. Please check the inputs.'}
