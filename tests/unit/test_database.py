import sqlite3

import pytest

from readingapp.models.database import base


def test_get_close_db(app):
    with app.app_context():
        db = base.get_database()
        assert db is base.get_database()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)
