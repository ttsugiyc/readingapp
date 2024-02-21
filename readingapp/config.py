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


def set_config(app: Flask, test_config=None):
    # 基本設定→設定ファイル読込→テスト設定読込
    app.config.from_mapping(
        CONFIG = os.path.join(app.instance_path, 'config.json'),
        IMAGE_FOLDER = os.path.join(app.static_folder, 'img'),
        DATABASE = os.path.join(app.instance_path, 'db.sqlite'),
        ADMIN_TOKEN = None,
        TESTING = test_config is not None,
    )

    if os.path.isfile(app.config['CONFIG']):
        app.config.from_file(app.config['CONFIG'], load=json.load)

    else:
        init_pass(app)

    if test_config:
        app.config.from_mapping(test_config)


def register_config(app: Flask, test_config=None):
    # コマンド追加→設定読み込み
    app.cli.add_command(init_pass_command)
    set_config(app, test_config)

    # ensure the instance/images folder exists
    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    if not os.path.isdir(app.config['IMAGE_FOLDER']):
        os.makedirs(app.config['IMAGE_FOLDER'])


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