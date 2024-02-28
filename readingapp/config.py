import os
import json
import secrets

import click
from flask import Flask, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash

from readingapp.exceptions import PasswordError


def save_pass(app: Flask):
    config = {
        'SECRET_KEY': app.config['SECRET_KEY'],
        'PASSWORD': app.config['PASSWORD'],
    }
    with open(app.config['CONFIG'], 'wt') as f:
        json.dump(config, f)


def init_pass(app: Flask):
    app.config.from_mapping(
        SECRET_KEY='dev',
        PASSWORD=generate_password_hash('admin'),
    )
    save_pass(app)


@click.command('init-pass')
def init_pass_command():
    """Clear the existing config file."""
    init_pass(current_app)
    click.echo('Initialized the configuration.')


def register_config(app: Flask, test_config=None):
    # コマンド追加→基本設定→設定ファイル読込
    app.cli.add_command(init_pass_command)

    app.config.from_mapping(
        CONFIG = os.path.join(app.instance_path, 'config.json'),
        IMAGE_FOLDER = os.path.join(app.static_folder, 'img'),
        DATABASE = os.path.join(app.instance_path, 'db.sqlite'),
        ADMIN_TOKEN = None,
        TESTING = test_config is not None,
    )

    if test_config:
        app.config.from_mapping(test_config)

    try:
        app.config.from_file(app.config['CONFIG'], load=json.load)

    except (OSError, json.decoder.JSONDecodeError):
        init_pass(app)
    
    if app.config['SECRET_KEY'] == 'dev':
        app.logger.warning('Starts with default settings')


def change_pass():
    """アプリから呼出"""
    if check_password_hash(current_app.config['PASSWORD'], request.form['password']):
        config = {
            'SECRET_KEY': secrets.token_hex(),
            'PASSWORD': generate_password_hash(request.form['new_password'])
        }
        current_app.config.from_mapping(config)
        save_pass(current_app)

    else:
        raise PasswordError
