import re
import secrets

from flask import request, g, session
from werkzeug.security import generate_password_hash, check_password_hash

from readingapp.exceptions import MyMessage, UniquenessError, PasswordError, LoginError
from readingapp.models.database.base import get_database


def validate_username(username: str):
    """文字幅16, ASCII, Not-Null"""
    if not username:
        raise MyMessage('ユーザー名を入力して下さい')

    if not re.fullmatch('[\u0000-\u007F]+', username):
        char = re.search('[^\u0000-\u007F]', username).group()
        raise MyMessage(f'ユーザー名に使用できない文字「{char}」が含まれています')

    if not len(username) <= 16:
        raise MyMessage('ユーザー名は16文字以内で入力して下さい')

    return username


def validate_email(email: str):
    """文字幅32, ASCII, empty->None"""
    if not email:
        return None

    if not re.fullmatch('[\u0000-\u007F]+', email):
        char = re.search('[^\u0000-\u007F]', email).group()
        raise MyMessage(f'メールアドレスに使用できない文字「{char}」が含まれています')

    if not len(email) <= 30:
        raise MyMessage('メールアドレスは30文字以内で入力して下さい')

    return email


def validate_password(password: str, salt: str):
    """Not-Null, password->hash, salt"""
    if not password:
        raise MyMessage('パスワードを入力して下さい')

    return generate_password_hash(password + salt)


def create_user():
    sql = 'INSERT INTO user (username, email, password, salt) VALUES (?, ?, ?, ?)'
    salt = secrets.token_hex(16)
    params = (
        validate_username(request.form.get('username')),
        validate_email(request.form.get('email')),
        validate_password(request.form.get('password'), salt),
        salt,
    )
    db = get_database()
    try:
        db.execute(sql, params)
        db.commit()

    except db.IntegrityError as error:
        db.rollback()
        if error.args == ('UNIQUE constraint failed: user.username',):
            raise UniquenessError('ユーザー名')
        if error.args == ('UNIQUE constraint failed: user.email',):
            raise UniquenessError('メールアドレス')
        raise error


def read_user(user_id):
    db = get_database()
    sql = 'SELECT * FROM user WHERE id = ?'
    user = db.execute(sql, (user_id,)).fetchone()
    return user


def update_username(user_id):
    sql = 'UPDATE user SET username = ? WHERE id = ?'
    db = get_database()
    new_username = validate_username(request.form.get('new_username'))
    try:
        db.execute(sql, (new_username, user_id))
        db.commit()

    except db.IntegrityError as error:
        db.rollback()
        if error.args == ('UNIQUE constraint failed: user.username',):
            raise UniquenessError('ユーザー名')
        raise error


def update_user_email(user_id):
    sql = 'UPDATE user SET email = ? WHERE id = ?'
    db = get_database()
    new_email = validate_email(request.form.get('new_email'))
    try:
        db.execute(sql, (new_email, user_id))
        db.commit()

    except db.IntegrityError as error:
        db.rollback()
        if error.args == ('UNIQUE constraint failed: user.email',):
            raise UniquenessError('メールアドレス')
        raise error


def update_user_password(user_id):
    db = get_database()
    sql = 'SELECT salt FROM user WHERE id = ?'
    salt = db.execute(sql, (user_id,)).fetchone()['salt']

    sql = 'UPDATE user SET password = ? WHERE id = ?'
    new_password = validate_password(request.form.get('new_password'), salt)
    db.execute(sql, (new_password, user_id))
    db.commit()


def auth_user():
    return check_password_hash(g.user['password'], request.form.get('password') + g.user['salt'])


def update_username_by_self():
    if auth_user():
        update_username(g.user['id'])
    else:
        raise PasswordError()


def update_user_email_by_self():
    if auth_user():
        update_user_email(g.user['id'])
    else:
        raise PasswordError()


def update_user_password_by_self():
    if auth_user():
        update_user_password(g.user['id'])
    else:
        raise PasswordError()


def delete_user(user_id):
    db = get_database()
    sql = 'DELETE FROM post WHERE user_id = ?'
    db.execute(sql, (user_id,))
    sql = 'DELETE FROM user WHERE id = ?'
    db.execute(sql, (user_id,))
    db.commit()


def delete_user_by_self():
    if auth_user():
        delete_user(g.user['id'])
    else:
        raise PasswordError()


def login_as_user():
    db = get_database()
    sql = 'SELECT * FROM user WHERE username = ?'
    g.user = db.execute(sql, (request.form.get('username'),)).fetchone()

    if g.user and auth_user():
        session.clear()
        session['user_id'] = g.user['id']
    else:
        raise LoginError()


def search_user():
    keyword = request.form.get('keyword')
    region = request.form.get('region')
    sql = 'SELECT * FROM user'
    params = []

    if keyword:
        keyword = '%' + keyword + '%'
        if region == 'username':
            sql += ' WHERE username LIKE ?'
            params = [keyword]
        elif region == 'email':
            sql += ' WHERE email LIKE ?'
            params = [keyword]
        else:
            sql += ' WHERE username LIKE ? OR email LIKE ?'
            params = [keyword, keyword]

    db = get_database()
    users = db.execute(sql, params).fetchall()
    return users
