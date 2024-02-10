import os
import json
import secrets

import click
from flask import Flask, current_app, request
from werkzeug.security import generate_password_hash, check_password_hash


@click.command('init-pass')
def init_pass_command():
    """Clear the existing config file."""
    if os.path.isfile(current_app.config['CONFIG']):
        os.remove(current_app.config['CONFIG'])

    click.echo('Initialized the configuration.')


def register_config(app: Flask, test_config=None):
    app.cli.add_command(init_pass_command)
    if test_config is None:
        is_loaded = app.config.from_file(app.config['CONFIG'], load=json.load, silent=True)
        if is_loaded:
            app.config['INITIAL_SETTINGS'] = False
        else:
            app.config.from_file(app.config['DEFAULT_CONFIG'], load=json.load)
            app.logger.warning('Starts with the initial configuration.')

    else:
        app.config.from_mapping(test_config)
        app.logger.info('Starts with the test configuration.')


def set_config():
    if check_password_hash(current_app.config['PASSWORD'], request.form['password']):
        config = {
            'SECRET_KEY': secrets.token_hex(),
            'PASSWORD': generate_password_hash(request.form['new_password'])
        }

        with open(current_app.config['CONFIG'], 'wt') as f:
            json.dump(config, f, indent=2)
        return True

    return False