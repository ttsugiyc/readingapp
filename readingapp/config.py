import os
import json
import secrets

import click
from flask import Flask, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash

from readingapp.exceptions import PasswordError


def init_pass():
    if os.path.isfile(current_app.config['CONFIG']):
        os.remove(current_app.config['CONFIG'])


@click.command('init-pass')
def init_pass_command():
    """Clear the existing config file."""
    init_pass()
    click.echo('Initialized the configuration.')


def set_config(app: Flask, test_config=None):
    app.config.from_mapping(
        CONFIG = os.path.join(app.instance_path, 'config.json'),
        IMAGE_FOLDER = os.path.join(app.static_folder, 'img'),
        DATABASE = os.path.join(app.instance_path, 'db.sqlite'),
        ADMIN_TOKEN = None,
        SECRET_KEY = 'dev',
        PASSWORD = generate_password_hash('admin'),
    )

    if test_config is None:
        is_loaded = app.config.from_file(app.config['CONFIG'], load=json.load, silent=True)
        if not is_loaded:
            app.logger.warning('Starts with the initial configuration.')

    else:
        app.config.from_mapping(test_config)
        app.logger.info('Starts with the test configuration.')


def register_config(app: Flask, test_config=None):
    app.cli.add_command(init_pass_command)
    set_config(app, test_config)

    # ensure the instance/images folder exists
    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    if not os.path.isdir(app.config['IMAGE_FOLDER']):
        os.makedirs(app.config['IMAGE_FOLDER'])


def save_config():
    if check_password_hash(current_app.config['PASSWORD'], request.form['password']):
        config = {
            'SECRET_KEY': secrets.token_hex(),
            'PASSWORD': generate_password_hash(request.form['new_password'])
        }

        with open(current_app.config['CONFIG'], 'wt') as f:
            json.dump(config, f, indent=2)

    else:
        raise PasswordError