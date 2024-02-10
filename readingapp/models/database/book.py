from flask import current_app

from readingapp.models.database.base import get_database


def create_books(infos):
    db = get_database()
    sql = (
        'INSERT INTO book (title, isbn_13, authors, publisher, image_name)'
        ' VALUES (?, ?, ?, ?, ?)'
    )
    for info in infos:
        try:
            params = (
                info['title'],
                info['isbn_13'],
                info['authors'],
                info.get('publisher'),
                info.get('image_name')
            )
            db.execute(sql, params)
            db.commit()
            current_app.logger.info('Obtained book information from API.')

        except db.IntegrityError as e:
            print(e)
            db.rollback()
            current_app.logger.info('Information about this book is already available.')


def search_books(isbn_13):
    db = get_database()
    sql = 'SELECT * FROM book WHERE isbn_13 = ?'
    books = db.execute(sql, (isbn_13,)).fetchall()
    return books
