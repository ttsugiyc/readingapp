import os

import flask
from flask import testing
from werkzeug import security

from readingapp.models.database import base


def test_init_pass_command(app: flask.Flask,runner: testing.FlaskCliRunner):
    app.config.from_mapping(
        SECRET_KEY='test_init_pass_command',
        PASSWORD='test_init_pass_command'
    )
    with app.app_context():
        init_pass_result = runner.invoke(args=['init-pass'])
        assert 'Initialized the password.' in init_pass_result.output
        assert app.config['SECRET_KEY'] == 'dev'
        assert security.check_password_hash(app.config['PASSWORD'], 'admin')


def test_init_data_command(app: flask.Flask, runner: testing.FlaskCliRunner):
    path = os.path.join(app.config['IMAGE_FOLDER'], 'test_init_data_command')
    with open(path, 'wt') as f:
        f.write('test_init_data_command')

    sql = 'SELECT * FROM user'
    with app.app_context():
        init_data_result = runner.invoke(args=['init-data'])
        assert 'Initialized the database.' in init_data_result.output
        assert len(base.get_database().execute(sql).fetchall()) == 0
        assert not os.path.exists(path)
