from flask import Blueprint, flash, redirect, render_template, request, url_for

from readingapp.security import login_required, check_owner, issue_csrf_token, catch_csrf_token
from readingapp.exceptions import MyException
from readingapp.models.isbn import canonicalize_ISBN
from readingapp.models.api import request_books
from readingapp.models.database.post import create_post, read_post, update_post, delete_post, search_posts
from readingapp.models.database.book import create_books, search_books


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

    if not books:
        infos = request_books(isbn_13)
        create_books(infos)
        books = search_books(isbn_13)
    
    if not books:
        raise MyException('書籍情報を取得できませんでした')

    return books


def get_books_from_api():
    """
    データベースを検索せず、直接APIを利用（未使用）
    """
    isbn_13 = canonicalize_ISBN(request.form.get('isbn'))
    infos = request_books(isbn_13)
    create_books(infos)
    books = search_books(isbn_13)
    
    if not books:
        raise MyException('書籍情報を取得できませんでした')

    return books


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        catch_csrf_token()
        try:
            books = get_books()
            issue_csrf_token()
            return render_template('user/bookshelf/create.html', books=books)

        except MyException as e:
            flash(e.__str__(), category='error')

    issue_csrf_token()
    return render_template('user/bookshelf/create.html', books=[])


@bp.route('/select', methods=('POST',))
@login_required
def select():
    catch_csrf_token()
    try:
        create_post()
        flash('書籍を追加しました')

    except MyException as e:
        flash(e.__str__(), category='error')

    return redirect(url_for('bookshelf.index'))


@bp.route('/<int:post_id>/update', methods=('GET', 'POST'))
@login_required
def update(post_id):
    post = read_post(post_id)
    check_owner(post)

    if request.method == 'POST':
        catch_csrf_token()
        try:
            update_post(post_id)
            flash('読書記録を更新しました')
            return redirect(url_for('bookshelf.index'))

        except MyException as e:
            flash(e.__str__(), category='error')

    issue_csrf_token()
    return render_template('user/bookshelf/update.html', post=post)


@bp.route('/<int:post_id>/delete', methods=('POST',))
@login_required
def delete(post_id):
    catch_csrf_token()
    post = read_post(post_id)
    check_owner(post)
    delete_post(post_id)
    flash('書籍を削除しました')
    return redirect(url_for('bookshelf.index'))
