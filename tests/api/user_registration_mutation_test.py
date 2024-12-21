import pytest
from starlette.testclient import TestClient

from src.main import app


@pytest.fixture
def client_gql():
    return TestClient(app)


def test_successful_user_registration_with_valid_data(client_gql):
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
            }
        }
    '''

    variables = {
        'name': 'John',
        'lastName': 'Smith',
        'username': 'John.smith',
        'email': 'John.smith@example.com',
        'mobilePhone': '3111111111',
        'password': 'password_example',
    }
    response = client_gql.post(
        '/graphql', json={'query': mutation, 'variables': variables},
    )

    data = response.json()
    assert data['registerUser']['result'] == 'User registered successfully.'
