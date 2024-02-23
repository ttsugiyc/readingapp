import functools
import secrets

from flask import current_app, g, request, session, redirect, url_for
from werkzeug.exceptions import abort

from readingapp.models.database.user import read_user


def protect_from_csrf():
    if request.method == 'POST':
        if request.form.get('token') != session.get('token'):
            abort(401)

    session['token'] = secrets.token_hex()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        user_id = session.get('user_id')
        if user_id is None:
            return redirect(url_for('auth.login'))

        g.user = read_user(user_id)
        if g.user is None:
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


def check_owner(post):
    """
    投稿が存在するか、本人の物か確認する
    直接URLに入力される可能性があるため
    """
    if post is None:
        abort(404)

    if post['user_id'] != g.user['id']:
        abort(403)
