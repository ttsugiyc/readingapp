import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from readingapp.models.database.user import create_user, read_user, login_user
from readingapp.models.exceptions import MyException


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        try:
            create_user()
            return redirect(url_for('auth.login'))
        
        except MyException as e:
            flash(e.__str__(), category='error')

    return render_template('user/auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        if login_user():
            return redirect(url_for('index'))

        else:
            flash('ログインできませんでした', category='error')

    return render_template('user/auth/login.html')


@bp.before_app_request
def load_logged_in():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = read_user(user_id)


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
