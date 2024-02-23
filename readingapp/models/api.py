import mimetypes
import os
import random
import string

import requests
from flask import current_app


def request_image(url):
    response = requests.get(url)
    extension = mimetypes.guess_extension(response.headers['Content-Type'])
    if response.status_code != 200:
        current_app.logger.info(f'Invalid responce: {response.status_code}')
        return None

    if not extension:
        current_app.logger.info('Invalid responce: Extension is unknown.')
        return None

    for _ in range(10000):
        name = ''.join(random.choice(string.ascii_uppercase) for _ in range(10))
        name += extension
        path = os.path.join(current_app.config['IMAGE_FOLDER'], name)
        if not os.path.exists(path):
            break

    else:
        current_app.logger.warning('Image name conflict could not be resolved.')
        return None

    with open(path, 'wb') as local_file:
        local_file.write(response.content)
        current_app.logger.info(f'Save the image: {name}')
    return name


def translate_response(response, isbn_13):
    books = []
    if 'items' not in response:
        current_app.logger.debug('"items" not found in response.')
        return books

    for item in response['items']:
        info = item['volumeInfo']
        book = {}

        # titleとisbn_13は必須
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
                book['image_name'] = request_image(image_url)

        books.append(book)
    return books


def use_api(isbn_13):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_13}'
    return requests.get(url).json()


def request_books(isbn_13):
    response = use_api(isbn_13)
    return translate_response(response, isbn_13)
