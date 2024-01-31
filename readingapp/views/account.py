from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from werkzeug.exceptions import abort

from readingapp.models.database.user import (
    update_username_by_self, update_user_email_by_self,
    update_user_password_by_self, delete_user_by_self
)
from readingapp.views.auth import login_required
from readingapp.views import constants


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('/settings')
@login_required
def settings():
    return render_template('user/account/settings.html')


@bp.route('/username', methods=('GET', 'POST'))
@login_required
def username():
    if request.method == 'POST':
        error = update_username_by_self()
        if not error:
            return redirect(url_for('account.settings'))
        elif error == 1:
            flash(constants.USERNAME_INTEGRITY_ERROR)
        elif error == 2:
            flash(constants.PASSWORD_ERROR)
        else:
            abort(404)

    return render_template('user/account/username.html')


@bp.route('/email', methods=('GET', 'POST'))
@login_required
def email():
    if request.method == 'POST':
        error = update_user_email_by_self()
        if not error:
            return redirect(url_for('account.settings'))
        elif error == 1:
            flash(constants.EMAIL_INTEGRITY_ERROR)
        elif error == 2:
            flash(constants.PASSWORD_ERROR)
        else:
            abort(404)

    return render_template('user/account/email.html')


@bp.route('/password', methods=('GET', 'POST'))
@login_required
def password():
    if request.method == 'POST':
        error = update_user_password_by_self()
        if not error:
            return redirect(url_for('account.settings'))
        else:
            flash(constants.PASSWORD_ERROR)

    return render_template('user/account/password.html')


@bp.route('/delete', methods=('GET', 'POST'))
@login_required
def delete():
    if request.method == 'POST':
        error = delete_user_by_self()
        if not error:
            session.clear()
            return redirect(url_for('auth.login'))

        else:
            flash(constants.PASSWORD_ERROR)

    return render_template('user/account/delete.html')
