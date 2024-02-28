import pytest
import flask
from flask import testing


@pytest.mark.parametrize('path', (
    '/admin',
    '/admin/1/update',
    '/admin/1/username',
    '/admin/1/email',
    '/admin/1/password',
    '/admin/settings',
))
def test_login_required_get(client: testing.FlaskClient, path):
    response = client.get(path)
    assert response.headers['Location'] == '/admin/login'


@pytest.mark.parametrize('path', (
    '/admin',
    '/admin/1/username',
    '/admin/1/email',
    '/admin/1/password',
    '/admin/1/delete',
    '/admin/settings',
))
def test_login_required_post(client: testing.FlaskClient, path):
    response = client.post(path)
    assert response.headers['Location'] == '/admin/login'


def test_login(client: testing.FlaskClient, auth):
    assert client.get('/admin/login').status_code == 200

    with client:
        assert auth.admin_login().headers['Location'] == '/admin'
        assert 'admin' in flask.session


def test_login_failed(auth):
    response = auth.admin_login('invalid')
    assert response.status_code == 200
    assert 'ログインできませんでした'.encode() in response.data


def test_logout(client: testing.FlaskClient, auth):
    auth.admin_login()

    with client:
        auth.admin_logout()
        assert 'user_id' not in flask.session
        assert 'admin' not in flask.session
        assert 'token' not in flask.session


@pytest.mark.parametrize(
    ('region', 'keyword'),
    (
        ('username', 'test'),
        ('email', 'test@test'),
        ('all', 'test'),
    )
)
def test_index(client: testing.FlaskClient, auth, region, keyword):
    auth.admin_login()
    with client:
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'test' in response.data
        assert b'test@test' in response.data

        response = client.post(
            '/admin',
            data={'region': region, 'keyword': keyword, 'token': flask.session['token']}
        )
        assert response.status_code == 200
        assert b'test' in response.data
        assert b'other' not in response.data


def test_update(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/1/update').status_code == 200

        response = client.post(
            '/admin/1/delete',
            data={'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/admin'
    
    assert 'ログインできませんでした'.encode() in auth.login().data


def test_exists_required(client: testing.FlaskClient, auth):
    auth.admin_login()
    assert client.get('/admin/100/update').status_code == 404


def test_username(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/1/username').status_code == 200

        response = client.post(
            '/admin/1/username',
            data={'new_username': 'new_test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/admin/1/update'
    
        assert 'ログインできませんでした'.encode() in auth.login().data
        auth.login(username='new_test')
        assert flask.session.get('user_id') == 1


def test_username_failed(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/1/username').status_code == 200

        response = client.post(
            '/admin/1/username',
            data={'new_username': 'other', 'token': flask.session['token']}
        )
        assert 'そのユーザー名は既に使用されています'.encode() in response.data


def test_email(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/1/email').status_code == 200

        response = client.post(
            '/admin/1/email',
            data={'new_email': 'new_test@test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/admin/1/update'
    
    assert b'new_test@test' in client.get('/admin').data


def test_email_failed(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/1/email').status_code == 200

        response = client.post(
            '/admin/1/email',
            data={'new_email': 'other@other', 'token': flask.session['token']}
        )
        assert 'そのメールアドレスは既に使用されています'.encode() in response.data


def test_password(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/1/password').status_code == 200

        response = client.post(
            '/admin/1/password',
            data={'new_password': 'new_test', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/admin/1/update'
    
        assert 'ログインできませんでした'.encode() in auth.login().data
        auth.login(password='new_test')
        assert flask.session.get('user_id') == 1


def test_settings(client: testing.FlaskClient, auth, app):
    auth.admin_login()
    with client:
        assert client.get('/admin/settings').status_code == 200

        response = client.post(
            '/admin/settings',
            data={'password': 'admin', 'new_password': 'new_admin', 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/admin'
    
        assert 'ログインできませんでした'.encode() in auth.admin_login().data
        auth.admin_login(password='new_admin')
        assert flask.session['admin'] == app.config['ADMIN_TOKEN']


def test_settings_failed(client: testing.FlaskClient, auth):
    auth.admin_login()
    with client:
        assert client.get('/admin/settings').status_code == 200

        response = client.post(
            '/admin/settings',
            data={'password': 'invalid', 'new_password': 'other', 'token': flask.session['token']}
        )
        assert 'パスワードが違います'.encode() in response.data