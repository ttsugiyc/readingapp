import pytest

import flask
from flask import testing

from readingapp.models.database import base


def test_register(app: flask.Flask, client: testing.FlaskClient):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'email': 'a@a', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert base.get_database().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'email', 'password', 'message'), (
    ('', 'b@b', 'b', 'ユーザー名を入力して下さい'.encode()),
    ('あ', 'b@b', 'b', 'ユーザー名に使用できない文字「あ」が含まれています'.encode()),
    ('01234567890123456', 'b@b', 'b', 'ユーザー名は16文字以内で入力して下さい'.encode()),
    ('test', 'b@b', 'b', 'そのユーザー名は既に使用されています'.encode()),

    ('b', 'あ@b', 'b', 'メールアドレスに使用できない文字「あ」が含まれています'.encode()),
    ('b', '01234567890123456789@0123456789', 'b', 'メールアドレスは30文字以内で入力して下さい'.encode()),
    ('b', 't@t', 'b', 'そのメールアドレスは既に使用されています'.encode()),
))
def test_register_validate_input(client: flask.Flask, username, email, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'email': email, 'password': password}
    )
    assert message in response.data


def test_logout(client: flask.Flask, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in flask.session
        assert 'admin' not in flask.session
        assert 'token' not in flask.session
