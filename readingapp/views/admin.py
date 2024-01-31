import functools

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, current_app
from werkzeug.security import check_password_hash

from readingapp.models.config import set_config
from readingapp.models.database.user import (
    read_user, search_user, delete_user,
    update_username, update_user_email, update_user_password
)
from readingapp.views import constants


bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required_as_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin.login'))

        return view(**kwargs)
    return wrapped_view


@bp.route('/', methods=('GET', 'POST'))
@login_required_as_admin
def index():
    users = search_user()
    return render_template('admin/users/index.html', users=users)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if check_password_hash(current_app.config['PASSWORD'], request.form['password']):
            session.clear()
            session['admin'] = True
            return redirect(url_for('admin.index'))
        else:
            flash(constants.LOGIN_ERROR)

    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('admin.login'))


@bp.route('/<int:user_id>/update/')
@login_required_as_admin
def update(user_id):
    user = read_user(user_id)
    return render_template('admin/users/update.html', user=user)


@bp.route('/<int:user_id>/username', methods=('GET', 'POST',))
def username(user_id):
    if request.method == 'POST':
        error = update_username(user_id)
        if not error:
            return redirect(url_for('admin.update', user_id=user_id))
        else:
            flash(constants.USERNAME_INTEGRITY_ERROR)

    user = read_user(user_id)
    return render_template('admin/users/username.html', user=user)


@bp.route('/<int:user_id>/email', methods=('GET', 'POST',))
def email(user_id):
    if request.method == 'POST':
        error = update_user_email(user_id)
        if not error:
            return redirect(url_for('admin.update', user_id=user_id))
        else:
            flash(constants.EMAIL_INTEGRITY_ERROR)

    user = read_user(user_id)
    return render_template('admin/users/email.html', user=user)


@bp.route('/<int:user_id>/password', methods=('GET', 'POST',))
def password(user_id):
    if request.method == 'POST':
        update_user_password(user_id)
        return redirect(url_for('admin.update', user_id=user_id))

    user = read_user(user_id)
    return render_template('admin/users/password.html', user=user)


@bp.route('/<int:user_id>/delete', methods=('POST',))
@login_required_as_admin
def delete(user_id):
    delete_user(user_id)
    return redirect(url_for('admin.index'))


@bp.route('/settings', methods=('GET', 'POST'))
@login_required_as_admin
def settings():
    if request.method == 'POST':
        error = set_config()
        if not error:
            return redirect(url_for('admin.index'))
        else:
            flash(constants.PASSWORD_ERROR)

    return render_template('admin/settings.html')
