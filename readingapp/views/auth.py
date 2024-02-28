from flask import Blueprint, request, session, flash, redirect, render_template, url_for

from readingapp.exceptions import MyMessage
from readingapp.models.database.user import create_user, login_as_user


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        try:
            create_user()
            flash('アカウントを作成しました')
            return redirect(url_for('auth.login'))
        
        except MyMessage as e:
            flash(e.__str__(), category='error')

    return render_template('user/auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            login_as_user()
            return redirect(url_for('index'))

        except MyMessage as e:
            flash(e.__str__(), category='error')

    return render_template('user/auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash('ログアウトしました')
    return redirect(url_for('auth.login'))
