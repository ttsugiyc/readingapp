import os
import shutil
import tempfile

import pytest
import flask

import readingapp
from readingapp.models.database import base


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    conf_fd, conf_path = tempfile.mkstemp()
    img_path = tempfile.mkdtemp()
    db_fd, db_path = tempfile.mkstemp()

    app = readingapp.create_app({
        'CONFIG': conf_path,
        'IMAGE_FOLDER': img_path,
        'DATABASE': db_path,
    })

    with app.app_context():
        base.init_data()
        base.get_database().executescript(_data_sql)

    yield app

    os.close(conf_fd)
    os.unlink(conf_path)
    shutil.rmtree(img_path)
    os.close(db_fd)
    os.unlink(db_path)


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


@pytest.fixture
def auth(client):
    return AuthActions(client)
