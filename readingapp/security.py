import functools
import secrets

from flask import current_app, g, request, session, redirect, url_for
from werkzeug.exceptions import abort, NotFound

from readingapp.models.database.user import read_user


def protect_from_csrf():
    if request.method == 'POST':
        if request.form.get('token') != session.get('token'):
            abort(401)

    session['token'] = secrets.token_hex(16)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect(url_for('auth.login'))

        try:
            g.user = read_user(user_id)
        except NotFound:
            return redirect(url_for('auth.login'))

        protect_from_csrf()
        return view(**kwargs)

    return wrapped_view


def login_required_as_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        admin_token = current_app.config['ADMIN_TOKEN']
        if admin_token is None or admin_token != session.get('admin'):
            return redirect(url_for('admin.login'))

        protect_from_csrf()
        return view(**kwargs)

    return wrapped_view
