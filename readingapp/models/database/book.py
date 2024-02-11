import os

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
            current_app.logger.debug('Obtained book information from API.')

        except db.IntegrityError:
            db.rollback()
            if info.get('image_name'):
                image_path = os.path.join(current_app.config['IMAGE_FOLDER'], info['image_name'])
                os.remove(image_path)
            current_app.logger.debug('Information about this book is already available.')


def search_books(isbn_13):
    db = get_database()
    sql = 'SELECT * FROM book WHERE isbn_13 = ?'
    books = db.execute(sql, (isbn_13,)).fetchall()
    return books
