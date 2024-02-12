import sqlite3

import pytest

from readingapp.models.database.base import get_database


def test_get_close_db(app):
    with app.app_context():
        db = get_database()
        assert db is get_database()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_data():
        Recorder.called = True

    monkeypatch.setattr('readingapp.models.database.base.init_data', fake_init_data)
    init_data_result = runner.invoke(args=['init-data'])
    assert 'database' in init_data_result.output
    assert Recorder.called
