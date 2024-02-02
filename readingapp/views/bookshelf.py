from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from readingapp.views.auth import login_required
from readingapp.models.isbn import canonicalize_ISBN
from readingapp.models.database.post import create_post, read_post, update_post, delete_post, search_posts
from readingapp.models.database.book import create_books, search_books
from readingapp.models.api import request_books
from readingapp.views import constants


bp = Blueprint('bookshelf', __name__)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    posts = search_posts()
    return render_template('user/bookshelf/index.html', posts=posts)


def get_books():
    """
    データベースを検索→見つからなければAPIを利用
    """
    isbn_13 = canonicalize_ISBN(request.form.get('isbn'))
    books = search_books(isbn_13)
    error = None

    if not isbn_13:
        error = constants.ISBN_ERROR

    elif not books:
        infos = request_books(isbn_13)
        create_books(infos)
        books = search_books(isbn_13)
        if not books:
            error = constants.API_ERROR

    return books, error


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        books, error = get_books()
        if not error:
            return render_template('user/bookshelf/create.html', books=books)

        flash(error)
    return render_template('user/bookshelf/create.html', books=[])


@bp.route('/<int:book_id>/select', methods=('POST',))
@login_required
def select(book_id):
    error = create_post(book_id)
    if error:
        flash(constants.BOOK_INTEGRITY_ERROR)
    return redirect(url_for('bookshelf.index'))


def check_owner(post):
    """
    投稿が存在するか、本人の物か確認する
    直接リクエストされる可能性があるため
    """
    if post is None:
        abort(404)

    if post['user_id'] != g.user['id']:
        abort(403)


@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = read_post(post_id)
    check_owner(post)

    if request.method == 'POST':
        update_post(post_id)
        return redirect(url_for('bookshelf.index'))

    return render_template('user/bookshelf/update.html', post=post)


@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    post = read_post(post_id)
    check_owner(post)
    delete_post(post_id)
    return redirect(url_for('bookshelf.index'))
