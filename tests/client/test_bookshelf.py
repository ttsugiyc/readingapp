import json
import os

import requests.models
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
    assert response.headers['Location'] == '/auth/login'


@pytest.mark.parametrize('path', (
    '/',
    '/create',
    '/select',
    '/1/update',
    '/1/delete',
))
def test_login_required_post(client: testing.FlaskClient, path):
    response = client.post(path)
    assert response.headers['Location'] == '/auth/login'


def test_index_get(client: testing.FlaskClient, auth):
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
    assert b'title2' in response.data


@pytest.mark.parametrize(
    ('region', 'status', 'keyword'),
    (
        ('all', 'all', '1'),
        ('title', 'all', 'title1'),
        ('authors', 'all', 'authors1'),
        ('publisher', 'all', 'publisher1'),
        ('comment', 'all', 'comment1'),
        ('all', 'finished', ''),
    )
)
def test_index_post(client: testing.FlaskClient, auth, region, status, keyword):
    auth.login()
    with client:
        assert client.get('/').status_code == 200
        response = client.post(
            '/',
            data={
                'sort': 'modified', 'region': region, 'status': status,
                'keyword': keyword, 'token': flask.session['token']
            }
        )
        assert b'title1' in response.data
        assert b'title2' not in response.data


def fake_search_by_api(isbn):
    if isbn == '9784042118046' or isbn == '4042118046':
        path = os.path.join(os.path.dirname(__file__), 'alice.json')
        with open(path, encoding='utf8') as f:
            data = json.load(f)
        return data

    else:
        return {}


def fake_get_image_by_api(url):
    response = requests.models.Response()
    response.status_code = 200
    response.headers['Content-Type'] = 'image/jpeg'
    response._content = b'image'
    return response


@pytest.mark.parametrize(
    ('book_id', 'isbn', 'title'),
    (
        ('4', '9784042118046', '鏡の国のアリス'.encode()),
        ('4', '4042118046', '鏡の国のアリス'.encode()),
        ('3', '0123456789036', b'title3'),
    )
)
def test_create(client: testing.FlaskClient, auth, monkeypatch, book_id, isbn, title):
    monkeypatch.setattr('readingapp.models.api.search_by_api', fake_search_by_api)
    monkeypatch.setattr('readingapp.models.api.get_image_by_api', fake_get_image_by_api)
    auth.login()
    with client:
        assert client.get('/create').status_code == 200
        response = client.post(
            '/create',
            data={'isbn': isbn, 'token': flask.session['token']}
        )
        assert title in response.data
        response = client.post(
            '/select',
            data={'book_id': book_id, 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/'

    assert title in client.get('/').data


@pytest.mark.parametrize(
    ('isbn', 'message'),
    (
        ('0', 'ISBN コードが正しくありません'.encode()),
        ('0000000000000', '書籍情報を取得できませんでした'.encode()),
        ('0000000000001', 'ISBN コードが正しくありません'.encode()),
        ('000000000000a', 'ISBN コードが正しくありません'.encode()),
        ('0000000000', '書籍情報を取得できませんでした'.encode()),
        ('0000000001', 'ISBN コードが正しくありません'.encode()),
        ('a000000000', 'ISBN コードが正しくありません'.encode()),
        ('000000000x', 'ISBN コードが正しくありません'.encode()),
    )
)
def test_create_falied(client: testing.FlaskClient, auth, monkeypatch, isbn, message):
    monkeypatch.setattr('readingapp.models.api.search_by_api', fake_search_by_api)
    monkeypatch.setattr('readingapp.models.api.get_image_by_api', fake_get_image_by_api)
    auth.login()
    with client:
        assert client.get('/create').status_code == 200
        response = client.post(
            '/create',
            data={'isbn': isbn, 'token': flask.session['token']}
        )
        assert response.status_code == 200
        assert message in response.data


def test_select_falied(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        client.get('/create')
        response = client.post(
            '/select',
            data={'book_id': 1, 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/'
        response = client.get('/')
        assert '登録済みの書籍です'.encode() in response.data


@pytest.mark.parametrize(
    ('post_id', 'status', 'comment'),
    (
        ('1', None, 'test_update1'),
        ('2', 'finished', 'test_update2'),
        ('1', 'finished', '0'*1000)
    )
)
def test_update(client: testing.FlaskClient, auth, post_id, status, comment):
    auth.login()
    with client:
        url = f'/{post_id}/update'
        assert client.get(url).status_code == 200
        response = client.post(
            url,
            data={'status': status, 'comment': comment, 'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/'

        response = client.get(url)
        if status:
            assert '>読了</p>'.encode() in response.data
        else:
            assert '>読了</p>'.encode() not in response.data
        assert comment.encode() in response.data


def test_update_falied(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        url = '/1/update'
        client.get(url)
        response = client.post(url, data={'comment': '0'*1001, 'token': flask.session['token']})
        assert response.status_code == 200
        assert 'コメントは1000文字以内で入力して下さい'.encode() in response.data


def test_delete(client: testing.FlaskClient, auth):
    auth.login()
    with client:
        client.get('/1/update')
        response = client.post(
            '/1/delete',
            data={'token': flask.session['token']}
        )
        assert response.headers['Location'] == '/'
        assert b'title1' not in client.get('/').data


def test_owner_required(client: testing.FlaskClient, auth):
    auth.login()
    assert client.get('/3/update').status_code == 403
    with client:
        client.get('/')
        response = client.post(
            '/3/update',
            data={'status': 'finished', 'comment': 'forbidden', 'token': flask.session['token']}
        )
        assert response.status_code == 403

        client.get('/')
        response = client.post(
            '/3/delete',
            data={'token': flask.session['token']}
        )
        assert response.status_code == 403


@pytest.mark.parametrize('path', ('/100/update',))
def test_exists_required(client: testing.FlaskClient, auth, path):
    auth.login()
    assert client.get(path).status_code == 404
