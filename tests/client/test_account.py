import pytest
import flask
from flask import testing


@pytest.mark.parametrize('path', (
    '/account/settings',
    '/account/username',
    '/account/email',
    '/account/password',
    '/account/delete',
))
def test_login_required_get(client: testing.FlaskClient, path):
    response = client.get(path)
    assert response.headers['Location'] == '/auth/login'


@pytest.mark.parametrize('path', (
    '/account/username',
    '/account/email',
    '/account/password',
    '/account/delete',
))
def test_login_required_post(client: testing.FlaskClient, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'


def test_settings(client: testing.FlaskClient, auth):
    auth.login()
    assert client.get('/account/settings').status_code == 200


def test_username(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        # ユーザー名変更画面の表示
        assert client.get('/account/username').status_code == 200

        # ユーザー名変更時にアカウント設定画面に遷移
        response = client.post(
            '/account/username',
            data={'new_username': 'new_test', 'password': 'test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/account/settings'

    # 元のユーザー情報でログインできなくなる
    auth.logout()
    assert auth.login().status_code == 200

    # 新しいユーザー情報でログインできる
    response = client.post(
        '/auth/login',
        data={'username': 'new_test', 'password': 'test'}
    )
    assert response.headers['Location'] == '/'


@pytest.mark.parametrize(('new_username', 'password', 'message'), (
    ('other', 'test', 'そのユーザー名は既に使用されています'.encode()),
    ('new_test', 'invalid', 'パスワードが違います'.encode()),
))
def test_username_falied(client: testing.FlaskClient, auth, new_username, password, message):
    auth.login()
    with client:
        client.get('/account/username')
        response = client.post(
            '/account/username',
            data={'new_username': new_username, 'password': password, 'token': flask.session['token']}
        )
        assert response.status_code == 200
        assert message in response.data


def test_email(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        # メールアドレス変更画面の表示
        assert client.get('/account/email').status_code == 200

        # メールアドレス変更時にアカウント設定画面に遷移
        response = client.post(
            '/account/email',
            data={'new_email': 'new_test@test', 'password': 'test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/account/settings'

    # メールアドレスの変更が確認できる
    assert b'new_test@test' in client.get('/account/settings').data


@pytest.mark.parametrize(('new_email', 'password', 'message'), (
    ('other@other', 'test', 'そのメールアドレスは既に使用されています'.encode()),
    ('new_email', 'invalid', 'パスワードが違います'.encode()),
))
def test_email_falied(client: testing.FlaskClient, auth, new_email, password, message):
    auth.login()
    with client:
        client.get('/account/email')
        response = client.post(
            '/account/email',
            data={'new_email': new_email, 'password': password, 'token': flask.session['token']}
        )
        assert response.status_code == 200
        assert message in response.data


def test_password(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        # パスワード変更画面の表示
        assert client.get('/account/password').status_code == 200

        # パスワード変更時にアカウント設定画面に遷移
        response = client.post(
            '/account/password',
            data={'new_password': 'new_test', 'password': 'test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/account/settings'

    # 元のユーザー情報でログインできなくなる
    auth.logout()
    assert auth.login().status_code == 200

    # 新しいユーザー情報でログインできる
    response = client.post(
        '/auth/login',
        data={'username': 'test', 'password': 'new_test'}
    )
    assert response.headers['Location'] == '/'


def test_password_falied(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        client.get('/account/password')
        response = client.post(
            '/account/password',
            data={'new_password': 'new_test', 'password': 'invalid', 'token': flask.session['token']}
        )
        assert response.status_code == 200
        assert 'パスワードが違います'.encode() in response.data


def test_delete(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        # 削除画面の表示
        assert client.get('/account/delete').status_code == 200

        # アカウント削除すると、ログアウトした後ログイン画面に遷移
        response = client.post(
            '/account/delete',
            data={'password': 'test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/auth/login'

    # ログインできなくなる
    response = auth.login()
    assert response.status_code == 200
