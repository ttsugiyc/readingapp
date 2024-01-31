import re

from flask import current_app, request, g
from werkzeug.security import generate_password_hash, check_password_hash

from readingapp.models.database.connection import get_database


def empty_to_none(string: str):
    """Not Null制約を活用するため、空の文字列をNoneに変換したい"""
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
        return 0

    except db.IntegrityError as error:
        db.rollback()
        current_app.logger.info(error)
        if re.search('username$', error.args[0]):
            return 1
        if re.search('email$', error.args[0]):
            return 2
        return 255


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
        return 0
    except db.IntegrityError as error:
        db.rollback()
        current_app.logger.info(error)
        return 1


def update_user_email(user_id):
    sql = 'UPDATE user SET email = ? WHERE id = ?'
    db = get_database()
    new_email = empty_to_none(request.form.get('new_email'))
    try:
        db.execute(sql, (new_email, user_id))
        db.commit()
        return 0
    except db.IntegrityError as error:
        db.rollback()
        current_app.logger.info(error)
        return 1


def update_user_password(user_id):
    sql = 'UPDATE user SET password = ? WHERE id = ?'
    db = get_database()
    new_password = generate_password_hash(request.form.get('new_password'))
    db.execute(sql, (new_password, user_id))
    db.commit()
    return 0


def update_username_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        return update_username(g.user['id'])
    return 2


def update_user_email_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        return update_user_email(g.user['id'])
    return 2


def update_user_password_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        return update_user_password(g.user['id'])
    return 2


def delete_user(user_id):
    db = get_database()
    sql = 'DELETE FROM user WHERE id = ?'
    db.execute(sql, (user_id,))
    sql = 'DELETE FROM post WHERE user_id = ?'
    db.execute(sql, (user_id,))
    db.commit()
    return 0


def delete_user_by_self():
    if check_password_hash(g.user['password'], request.form.get('password')):
        return delete_user(g.user['id'])
    return 2


def request_user_id():
    db = get_database()
    sql = 'SELECT * FROM user WHERE username = ?'
    user = db.execute(sql, (request.form.get('username'),)).fetchone()
    if user and check_password_hash(user['password'], request.form.get('password')):
        return user['id']
    else:
        return None


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
