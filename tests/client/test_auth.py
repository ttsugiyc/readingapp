import pytest

import flask
from flask import testing

from readingapp.models.database import base


@pytest.mark.parametrize(
    ('username', 'email', 'password'),
    (
        ('a', 'a@a', 'a'),
        ('a', None, 'a'),
        ('0123456789012345', 'a@a', 'a'),
        ('a', '01234567890123456789@012345678', 'a'),
    )
)
def test_register(app: flask.Flask, client: testing.FlaskClient, username, email, password):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={'username': username, 'email': email, 'password': password}
    )
    assert response.headers['Location'] == '/auth/login'

    with app.app_context():
        assert base.get_database().execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone() is not None


@pytest.mark.parametrize(
    ('username', 'email', 'password', 'message'),
    (
        ('', 'a@a', 'a', 'ユーザー名を入力して下さい'.encode()),
        ('あ', 'a@a', 'a', 'ユーザー名に使用できない文字「あ」が含まれています'.encode()),
        ('01234567890123456', 'a@a', 'a', 'ユーザー名は16文字以内で入力して下さい'.encode()),
        ('test', 'a@a', 'a', 'そのユーザー名は既に使用されています'.encode()),

        ('a', 'あ@a', 'a', 'メールアドレスに使用できない文字「あ」が含まれています'.encode()),
        ('a', '01234567890123456789@0123456789', 'a', 'メールアドレスは30文字以内で入力して下さい'.encode()),
        ('a', 'test@test', 'a', 'そのメールアドレスは既に使用されています'.encode()),

        ('a', 'a@a', '', 'パスワードを入力して下さい'.encode()),
    )
)
def test_register_validate_input(client: testing.FlaskClient, username, email, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'email': email, 'password': password}
    )
    assert response.status_code == 200
    assert message in response.data


def test_login(client: testing.FlaskClient, auth):
    assert client.get('/auth/login').status_code == 200

    with client:
        assert auth.login().headers['Location'] == '/'
        assert flask.session.get('user_id') == 1


@pytest.mark.parametrize(
    ('username', 'password'),
    (
        ('invalid', 'test'),
        ('test', 'invalid')
    )
)
def test_login_failed(auth, username, password):
    response = auth.login(username, password)
    assert response.status_code == 200
    assert 'ログインできませんでした'.encode() in response.data


def test_logout(client: flask.Flask, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in flask.session
        assert 'admin' not in flask.session
        assert 'token' not in flask.session
