import pytest
import flask
from flask import testing


@pytest.mark.parametrize('path', (
    '/',
    '/create',
    '/1/update',
))
def test_login_required_get(client: testing.FlaskClient, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/',
    '/create',
    '/select',
    '/1/update',
    '/1/delete',
))
def test_login_required_post(client: testing.FlaskClient, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_index(client: testing.FlaskClient, auth):
    auth.login()
    response = client.get('/')
    assert 'ログアウト'.encode() in response.data

    # 投稿が確認できること
    assert b'title1' in response.data
    assert b'authors1' in response.data
    assert b'publisher1' in response.data
    assert b'test\ncomment' in response.data
    assert b'src="/static/img/image1"' in response.data
    assert b'href="/1/update"' in response.data


def test_owner_required(client: testing.FlaskClient, auth):
    auth.login()
    # current user can't see other user's post
    assert client.get('/3/update').status_code == 403
    # current user doesn't see edit link
    assert b'href="/3/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/100/update',
))
def test_exists_required(client: testing.FlaskClient, auth, path):
    auth.login()
    assert client.get(path).status_code == 404
