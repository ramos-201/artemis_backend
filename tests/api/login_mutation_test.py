from pytest import mark


@mark.asyncio
async def test_successful_login_with_valid_username(mock_prepare_db, client_api):
    mutation_login = '''
        mutation(
            $username: String!,
            $password: String!,
        ) {
            login(
                username: $username,
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

    mutation_variables = {
        'username': 'John.smith',
        'password': 'password_example',
    }
    response = client_api.post('/graphql', json={'query': mutation_login, 'variables': mutation_variables})
    response_data = response.json()
    result_login = response_data['login']
    assert result_login['ok'] is True
    assert result_login['message'] == 'Login successful.'
    assert result_login['user']['id'] is not None

    # user_data = await User.get(id=result_login['user']['id'])
    # assert user_data.username == mutation_variables['username']
    # assert user_data.email == mutation_variables['email']
