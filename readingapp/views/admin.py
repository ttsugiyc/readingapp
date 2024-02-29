import secrets

from flask import Blueprint, flash, redirect, render_template, g, request, session, url_for, current_app
from werkzeug.security import check_password_hash

from readingapp.security import login_required_as_admin
from readingapp.exceptions import Message, LoginError
from readingapp.config import change_pass
from readingapp.models.database.user import (
    read_user, search_user, delete_user,
    update_username, update_user_email, update_user_password
)


bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('', methods=('GET', 'POST'))
@login_required_as_admin
def index():
    users = search_user()
    return render_template('admin/users/index.html', users=users)


def login_as_admin():
    if check_password_hash(current_app.config['PASSWORD'], request.form['password']):
        token = secrets.token_hex(16)
        session.clear()
        session['admin'] = token
        current_app.config['ADMIN_TOKEN'] = token

    else:
        raise LoginError()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            login_as_admin()
            return redirect(url_for('admin.index'))

        except Message as e:
            flash(e.__str__(), category='error')

    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    current_app.config['ADMIN_TOKEN'] = None
    flash('ログアウトしました')
    return redirect(url_for('admin.login'))


@bp.route('/<int:user_id>/update')
@login_required_as_admin
def update(user_id):
    user = read_user(user_id)
    return render_template('admin/users/update.html', user=user)


@bp.route('/<int:user_id>/username', methods=('GET', 'POST',))
@login_required_as_admin
def username(user_id):
    if request.method == 'POST':
        try:
            update_username(user_id)
            flash('ユーザー名を変更しました')
            return redirect(url_for('admin.update', user_id=user_id))
        
        except Message as e:
            flash(e.__str__(), category='error')

    user = read_user(user_id)
    return render_template('admin/users/username.html', user=user)


@bp.route('/<int:user_id>/email', methods=('GET', 'POST',))
@login_required_as_admin
def email(user_id):
    if request.method == 'POST':
        try:
            update_user_email(user_id)
            flash('メールアドレスを変更しました')
            return redirect(url_for('admin.update', user_id=user_id))
        
        except Message as e:
            flash(e.__str__(), category='error')

    user = read_user(user_id)
    return render_template('admin/users/email.html', user=user)


@bp.route('/<int:user_id>/password', methods=('GET', 'POST',))
@login_required_as_admin
def password(user_id):
    if request.method == 'POST':
        update_user_password(user_id)
        flash('パスワードを変更しました')
        return redirect(url_for('admin.update', user_id=user_id))

    user = read_user(user_id)
    return render_template('admin/users/password.html', user=user)


@bp.route('/<int:user_id>/delete', methods=('POST',))
@login_required_as_admin
def delete(user_id):
    delete_user(user_id)
    flash('ユーザーを削除しました')
    return redirect(url_for('admin.index'))


@bp.route('/settings', methods=('GET', 'POST'))
@login_required_as_admin
def settings():
    if request.method == 'POST':
        try:
            change_pass()
            flash('設定を変更しました')
            return redirect(url_for('admin.index'))

        except Message as e:
            flash(e.__str__(), category='error')

    return render_template('admin/settings.html')
