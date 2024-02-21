import pytest

from flask import g, session

from readingapp.models.database.base import get_database


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'email': 'a@a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_database().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'message'), (
    ('', '', '', 'ユーザー名を入力して下さい'.encode('utf8')),
    ('あ', '', '', 'ユーザー名に使用できない文字「あ」が含まれています'.encode('utf8')),
    ('qwertyuiopasdfghj', '', '', 'ユーザー名は16文字以内で入力して下さい'.encode('utf8')),
    ('invalid', 'あ', 'test', 'メールアドレスに使用できない文字「あ」が含まれています'.encode('utf8')),
    ('invalid', 'qwertyuiopasdfghjklzxcvbnm@qwer', '', 'メールアドレスは30文字以内で入力して下さい'.encode('utf8')),
    ('invalid', 't@t', '', 'そのメールアドレスは既に使用されています'.encode('utf8')),
))
def test_register_validate_input(client, username, email, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'email': email, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session
