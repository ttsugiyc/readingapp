from flask import testing


def test_post_falied(client: testing.FlaskClient, auth):
    auth.login()
    response = client.post(
        '/',
        data={'region': 'all','status': 'finished', 'keyword': '', 'token': 'invalid'}
    )
    assert response.status_code == 401


def test_non_existent_user(client: testing.FlaskClient):
    with client.session_transaction() as session:
        session['user_id'] = 100

    assert client.get('/').headers['Location'] == '/auth/login'
