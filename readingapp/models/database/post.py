import unicodedata

from flask import g, request
from werkzeug.exceptions import abort

from readingapp.models.database.base import get_database
from readingapp.models.exceptions import MyException


def create_post(book_id):
    db = get_database()
    sql = 'INSERT INTO post (user_id, book_id) VALUES (?, ?)'
    try:
        db.execute(sql, (g.user['id'], book_id))
        db.commit()

    except db.IntegrityError as e:
        db.rollback()
        if e.args == ('UNIQUE constraint failed: post.user_id, post.book_id',):
            raise MyException('登録済みの書籍です')

        if e.args == ('FOREIGN KEY constraint failed',):
            abort(404)
        raise e


def read_post(post_id):
    db = get_database()
    sql = (
        'SELECT * FROM post JOIN book ON post.book_id = book.id'
        ' WHERE post.id = ?'
    )
    post = db.execute(sql, (post_id,)).fetchone()
    return post


def get_width(string: str):
    """半角文字幅1, 全角文字幅2"""
    width = 0
    for char in string:
        if unicodedata.east_asian_width(char) in 'FWA':
            width += 2
        else:
            width += 1
    return width


def validate_comment(comment: str):
    if not get_width(comment) <= 1000:
        raise MyException('コメントは1000文字以内で入力して下さい')
    return comment


def update_post(post_id):
    db = get_database()
    sql = (
        'UPDATE post SET comment = ?, status = ?,'
        ' modified = CURRENT_TIMESTAMP WHERE id = ?'
    )
    params = (
        validate_comment(request.form.get('comment')),
        'status' in request.form,
        post_id
    )
    db.execute(sql, params)
    db.commit()


def delete_post(post_id):
    db = get_database()
    sql = 'DELETE FROM post WHERE id = ?'
    db.execute(sql, (post_id,))
    db.commit()


def add_keyword(sql, params):
    keyword = request.form.get('keyword')
    region = request.form.get('region')

    if keyword:
        keyword = '%' + keyword + '%'
        params += [keyword]
        if region == 'title':
            sql += ' AND book.title LIKE ?'
        elif region == 'authors':
            sql += ' AND book.authors LIKE ?'
        elif region == 'publisher':
            sql += ' AND book.publisher LIKE ?'
        elif region == 'comment':
            sql += ' AND post.comment LIKE ?'
        else:
            sql += (
                ' AND (book.title LIKE ? OR book.authors LIKE ?'
                ' OR book.publisher LIKE ? OR post.comment LIKE ?)'
            )
            params += [keyword, keyword, keyword]

    return sql, params


def add_status(sql, params):
    status = request.form.get('status')
    if status == 'finished':
        sql += ' AND post.status = ?'
        params += [1]
    elif status == 'not_finished':
        sql += ' AND post.status = ?'
        params += [0]
    return sql, params


def add_sort(sql):
    if request.form.get('sort') == 'created':
        sql += ' ORDER BY created DESC'
    else:
        sql += ' ORDER BY modified DESC'
    return sql


def search_posts():
    sql = (
        'SELECT * FROM post JOIN book ON post.book_id = book.id'
        ' WHERE post.user_id = ?'
    )
    params = [g.user['id']]
    sql, params = add_keyword(sql, params)
    sql, params = add_status(sql, params)
    sql = add_sort(sql)

    db = get_database()
    posts = db.execute(sql, params).fetchall()
    return posts
