import mimetypes
import os
import random
import string

import requests
from flask import current_app


def search_by_api(isbn_13):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_13}'
    return requests.get(url).json()


def get_image_by_api(url):
    return requests.get(url)


def get_image(url):
    # 画像取得->拡張子判定->ファイル名生成->画像保存->ファイル名出力
    response = get_image_by_api(url)
    if response.status_code != 200:
        current_app.logger.debug(f'Request failed: {response.status_code}')
        return None

    extension = mimetypes.guess_extension(response.headers['Content-Type'])
    if not extension:
        current_app.logger.debug('Request failed: Extension is unknown.')
        return None

    for _ in range(10000):
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        name += extension
        path = os.path.join(current_app.config['IMAGE_FOLDER'], name)
        if not os.path.exists(path):
            break
    else:
        current_app.logger.error('Could not generate image name.')
        return None

    with open(path, 'wb') as local_file:
        local_file.write(response.content)
        current_app.logger.debug(f'Save the image: {name}')
    return name


def translate_response(response, isbn_13):
    books = []
    if 'items' not in response:
        current_app.logger.debug('"items" not found in response.')
        return books

    for item in response['items']:
        info = item['volumeInfo']
        book = {}

        # title無しならば無視
        book['title'] = info.get('title')
        if not book['title']:
            current_app.logger.debug('"title" not found in response book.')
            continue
        book['isbn_13'] = isbn_13

        authors = ''
        for author in info.get('authors'):
            authors += author + ', '
        if authors:
            authors = authors[:-2]
        book['authors'] = authors

        book['publisher'] = info.get('publisher')

        book['image_name'] = None
        image_links = info.get('imageLinks')
        if image_links:
            image_url = image_links.get('thumbnail')
            if image_url:
                book['image_name'] = get_image(image_url)

        books.append(book)
    return books


def request_books(isbn_13):
    response = search_by_api(isbn_13)
    return translate_response(response, isbn_13)
