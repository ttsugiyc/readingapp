from flask import Blueprint, flash, redirect, render_template, request, url_for

from readingapp.models.exceptions import MyException
from readingapp.models.database.user import (
    update_username_by_self, update_user_email_by_self,
    update_user_password_by_self, delete_user_by_self
)
from readingapp.views.auth import login_required


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/settings')
@login_required
def settings():
    return render_template('user/account/settings.html')


@bp.route('/username', methods=('GET', 'POST'))
@login_required
def username():
    if request.method == 'POST':
        try:
            update_username_by_self()
            return redirect(url_for('account.settings'))

        except MyException as e:
            flash(e.__str__(), category='error')

    return render_template('user/account/username.html')


@bp.route('/email', methods=('GET', 'POST'))
@login_required
def email():
    if request.method == 'POST':
        try:
            update_user_email_by_self()
            return redirect(url_for('account.settings'))

        except MyException as e:
            flash(e.__str__(), category='error')

    return render_template('user/account/email.html')


@bp.route('/password', methods=('GET', 'POST'))
@login_required
def password():
    if request.method == 'POST':
        try:
            update_user_password_by_self()
            return redirect(url_for('account.settings'))

        except MyException as e:
            flash(e.__str__(), category='error')

    return render_template('user/account/password.html')


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'POST':
        try:
            delete_user_by_self()
            return redirect(url_for('auth.login'))

        except MyException as e:
            flash(e.__str__(), category='error')

    return render_template('user/account/delete.html')
