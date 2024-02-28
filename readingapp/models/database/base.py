import os
import sqlite3

import click
from flask import Flask, current_app, g


def get_database():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = true")

    return g.db


def close_database(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_data():
    db = get_database()

    with current_app.open_resource('models/database/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    for name in os.listdir(current_app.config['IMAGE_FOLDER']):
        os.remove(os.path.join(current_app.config['IMAGE_FOLDER'], name))


@click.command('init-data')
def init_data_command():
    """Clear the existing data and create new tables."""
    init_data()
    click.echo('Initialized the database.')


def register_database(app: Flask):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_data_command)

    if not os.path.isdir(app.config['IMAGE_FOLDER']):
        os.makedirs(app.config['IMAGE_FOLDER'])

    if not os.path.isfile(app.config['DATABASE']):
        with app.app_context():
            init_data()
