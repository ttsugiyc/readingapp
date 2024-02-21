import pytest
from readingapp.models.database.base import get_database


def test_index(client, auth):
    auth.login()
    response = client.get('/')
    assert 'ログアウト'.encode() in response.data
    assert b'test title' in response.data
    assert b'test authors' in response.data
    assert b'test publisher' in response.data
    assert b'test\ncomment' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/',
    '/create',
    '/1/update',
    '/account/settings',
    '/account/username',
    '/account/email',
    '/account/password',
))
def test_login_required(client, path):
    response = client.get(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_database()
        db.execute('UPDATE post SET user_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't see other user's post
    assert client.get('/1/update').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/2/update',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.get(path).status_code == 404
