from flask import request, g, session
from werkzeug.security import generate_password_hash, check_password_hash

from readingapp.models.database.base import get_database
from readingapp.models.exceptions import UniquenessError, PasswordError


def empty_to_none(string: str):
    """Not Null制約を活用するため、空の文字列をNoneに変換"""
    return string if not string == '' else None


def create_user():
    sql = 'INSERT INTO user (username, email, password) VALUES (?, ?, ?)'
    params = (
        empty_to_none(request.form.get('username')),
        empty_to_none(request.form.get('email')),
        generate_password_hash(request.form.get('password'))
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
    new_username = empty_to_none(request.form.get('new_username'))
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
    new_email = empty_to_none(request.form.get('new_email'))
    try:
        db.execute(sql, (new_email, user_id))
        db.commit()

    except db.IntegrityError as error:
        db.rollback()
        if error.args == ('UNIQUE constraint failed: user.email',):
            raise UniquenessError('メールアドレス')
        raise error


def update_user_password(user_id):
    sql = 'UPDATE user SET password = ? WHERE id = ?'
    db = get_database()
    new_password = generate_password_hash(request.form.get('new_password'))
    db.execute(sql, (new_password, user_id))
    db.commit()


def update_username_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        update_username(g.user['id'])
    else:
        raise PasswordError()


def update_user_email_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        update_user_email(g.user['id'])
    else:
        raise PasswordError()


def update_user_password_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        update_user_password(g.user['id'])
    else:
        raise PasswordError()


def delete_user(user_id):
    db = get_database()
    sql = 'DELETE FROM user WHERE id = ?'
    db.execute(sql, (user_id,))
    sql = 'DELETE FROM post WHERE user_id = ?'
    db.execute(sql, (user_id,))
    db.commit()


def delete_user_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        delete_user(g.user['id'])
    else:
        raise PasswordError()


def login_user():
    db = get_database()
    sql = 'SELECT * FROM user WHERE username = ?'
    user = db.execute(sql, (request.form.get('username'),)).fetchone()

    session.clear()
    if user and check_password_hash(user['password'], request.form.get('password')):
        session['user_id'] = user['id']
        return True
    else:
        return False


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
