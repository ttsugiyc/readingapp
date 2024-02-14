import functools
import secrets

from flask import current_app, g, request, session, redirect, url_for
from werkzeug.exceptions import abort


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def login_required_as_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        admin_token = current_app.config['ADMIN_TOKEN']
        if admin_token is None or admin_token != session.get('admin'):
            return redirect(url_for('admin.login'))

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


def protect_from_csrf(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if request.method == 'POST':
            if request.form.get('token') != session.pop('token'):
                abort(400)

        session['token'] = secrets.token_hex()
        return view(**kwargs)

    return wrapped_view
