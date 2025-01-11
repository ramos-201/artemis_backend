def test_successful_user_registration_with_valid_data(mock_prepare_db, client_app):
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
                data {
                    id
                }
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

    response = client_app.post('/graphql', json={'query': mutation, 'variables': variables})

    data = response.json()
    assert data['registerUser']['result'] == 'User registered successfully.'
    assert data['registerUser']['data']['id'] == '1'
