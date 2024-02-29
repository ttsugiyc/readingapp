import os
import shutil
import tempfile

import pytest
import flask

import readingapp
from readingapp.models.database import base


@pytest.fixture
def app():
    static_folder = tempfile.mkdtemp()
    instance_path = tempfile.mkdtemp()

    app = readingapp.create_app({}, static_folder, instance_path)

    sql_path = os.path.join(os.path.dirname(__file__), 'data.sql')
    with app.app_context():
        with open(sql_path, encoding='utf8') as f:
            base.get_database().executescript(f.read())

    yield app

    shutil.rmtree(instance_path)
    shutil.rmtree(static_folder)


@pytest.fixture
def client(app: flask.Flask):
    return app.test_client()


@pytest.fixture
def runner(app: flask.Flask):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')
    
    def admin_login(self, password='admin'):
        return self._client.post(
            '/admin/login',
            data={'password': password}
        )
    
    def admin_logout(self):
        return self._client.get('/admin/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
