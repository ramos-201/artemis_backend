from pytest import mark

from src.models import User


@mark.asyncio
async def test_successful_user_registration_with_valid_data(mock_prepare_db, client_app):
    mutation = '''
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
                result
                user {
                    id
                }
            }
        }
    '''

    mutation_variables = {
        'name': 'John',
        'lastName': 'Smith',
        'username': 'John.smith',
        'email': 'John.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password_example',
    }

    response = client_app.post('/graphql', json={'query': mutation, 'variables': mutation_variables})

    response_data = response.json()
    assert response_data['registerUser']['result'] == 'User registered successfully.'
    assert response_data['registerUser']['user']['id'] is not None

    user_created = await User.get(id=response_data['registerUser']['user']['id'])
    assert user_created.name == mutation_variables['name']
    assert user_created.last_name == mutation_variables['lastName']
    assert user_created.username == mutation_variables['username']
    assert user_created.email == mutation_variables['email']
    assert user_created.mobile_phone == mutation_variables['mobilePhone']
    assert user_created.password == mutation_variables['password']
    assert user_created.is_active_account is False
    assert user_created.date_account_activated is None
