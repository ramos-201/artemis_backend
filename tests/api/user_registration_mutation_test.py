from pytest import mark

from src.models import User
from tests.factory_test import UserFactory


mutation_register_user = '''
    mutation(
        $name: String!,
        $lastName: String!,
        $username: String!,
        $email: String!,
        $mobilePhone: String!,
        $password: String!,
    ) {
        registerUser(
            name: $name,
            lastName: $lastName,
            username: $username,
            email: $email,
            mobilePhone: $mobilePhone,
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
async def test_successful_user_registration_with_valid_data(mock_prepare_db, client_api):
    mutation_variables = {
        'name': 'John',
        'lastName': 'Smith',
        'username': 'John.smith',
        'email': 'John.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password_example',
    }

    response = client_api.post('/graphql', json={'query': mutation_register_user, 'variables': mutation_variables})
    response_data = response.json()

    result_register_user = response_data['registerUser']
    assert result_register_user['ok'] is True
    assert result_register_user['message'] == 'User registered successfully.'
    assert result_register_user['user']['id'] is not None

    user_created = await User.get(id=result_register_user['user']['id'])
    assert user_created.name == mutation_variables['name']
    assert user_created.last_name == mutation_variables['lastName']
    assert user_created.username == mutation_variables['username']
    assert user_created.email == mutation_variables['email']
    assert user_created.mobile_phone == mutation_variables['mobilePhone']
    assert user_created.password == mutation_variables['password']
    assert user_created.is_active_account is False
    assert user_created.date_account_activated is None


@mark.asyncio
async def test_error_when_user_already_exists_in_user_registration(mock_prepare_db, client_api):
    existing_user = await UserFactory.build()
    await existing_user.save()

    mutation_variables = {
        'name': existing_user.name,
        'lastName': existing_user.last_name,
        'username': existing_user.username,
        'email': existing_user.email,
        'mobilePhone': existing_user.mobile_phone,
        'password': existing_user. password,
    }

    response = client_api.post('/graphql', json={'query': mutation_register_user, 'variables': mutation_variables})
    response_data = response.json()

    result_register_user = response_data['registerUser']
    assert result_register_user['ok'] is False
    assert result_register_user['message'] == 'Error: mobile_phone data already exists'
    assert result_register_user['user'] is None


# TODO: integrate these tests
"""
- Cuando los campos se envian vacios o no se envian campos requeridos a nivel BD???
- cuando no se envian los campos requeridos a nivel GPQL o no se envian las variables???
"""
