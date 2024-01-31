import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.exceptions import abort

from readingapp.models.database.user import create_user, read_user, request_user_id
from readingapp.views import constants


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        error = create_user()

        if not error:
            return redirect(url_for("auth.login"))
        elif error == 1:
            flash(constants.USERNAME_INTEGRITY_ERROR)
        elif error == 2:
            flash(constants.EMAIL_INTEGRITY_ERROR)
        else:
            abort(404)

    return render_template('user/auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        user_id = request_user_id()

        if user_id is not None:
            session.clear()
            session['user_id'] = user_id
            return redirect(url_for('index'))

        flash(constants.LOGIN_ERROR)

    return render_template('user/auth/login.html')


@bp.before_app_request
def load_logged_in():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = read_user(user_id)

    g.admin = session.get('admin')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
