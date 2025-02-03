from pytest import mark

from src.models import User
from src.utils import PATH_API


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
    response = client_api.post(PATH_API, json={'query': mutation_register_user, 'variables': mutation_variables})
    response_json = response.json()

    assert response_json == {
        'registerUser': {
            'ok': True,
            'message': 'User registered successfully.',
            'user': {
                'id': '1',
            },
        },
    }

    user_created = await User.get(id=response_json['registerUser']['user']['id'])
    assert user_created.name == mutation_variables['name']
    assert user_created.last_name == mutation_variables['lastName']
    assert user_created.username == mutation_variables['username']
    assert user_created.email == mutation_variables['email']
    assert user_created.mobile_phone == mutation_variables['mobilePhone']
    assert user_created.password == mutation_variables['password']
    assert user_created.is_active_account is False
    assert user_created.date_account_activated is None


@mark.asyncio
async def test_error_when_user_already_exists_in_user_registration(
        mock_prepare_db, client_api, default_user_record_constructor,
):
    existing_user = await default_user_record_constructor

    mutation_variables = {
        'name': existing_user.name,
        'lastName': existing_user.last_name,
        'username': existing_user.username,
        'email': existing_user.email,
        'mobilePhone': existing_user.mobile_phone,
        'password': existing_user.password,
    }
    response = client_api.post(PATH_API, json={'query': mutation_register_user, 'variables': mutation_variables})
    assert response.json() == {
        'registerUser': {
            'ok': False,
            'message': 'The data for the field "mobile_phone" already exists.',
            'user': None,
        },
    }


@mark.asyncio
async def test_error_when_fields_are_empty_strings(mock_prepare_db, client_api):
    mutation_variables = {
        'name': '',
        'lastName': '',
        'username': '',
        'email': '',
        'mobilePhone': '',
        'password': '',
    }
    response = client_api.post(PATH_API, json={'query': mutation_register_user, 'variables': mutation_variables})
    assert response.json() == {
        'registerUser': {
            'ok': False,
            'message': 'The field "name" cannot be empty or contain only spaces.',
            'user': None,
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
    response = client_api.post(PATH_API, json={'query': mutation_register_user, 'variables': mutation_variables})
    assert response.json() == {'error': 'There was a problem with the fields provided. Please check the inputs.'}
