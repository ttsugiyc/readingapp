import os
import tempfile

import pytest
from readingapp import create_app
from readingapp.models.database.base import get_database, init_data


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'DATABASE': db_path,
        'IMAGE_FOLDER': os.path.join(os.path.dirname(__file__), 'static', 'img'),
        'CONFIG': os.path.join(os.path.dirname(__file__), 'test_config.json')
    })

    with app.app_context():
        init_data()
        get_database().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()