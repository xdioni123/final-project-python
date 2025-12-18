from flask import Blueprint, render_template, request

book_bp = Blueprint('book', __name__, template_folder='../templates')

@book_bp.route('/books')
def all_books():
    from database import db
    from models.book import Book

    genre_filter = request.args.get('genre')
    if genre_filter:
        books = Book.query.filter_by(genre=genre_filter).all()
    else:
        books = Book.query.all()
    return render_template('books.html', books=books)

@book_bp.route('/book/<int:book_id>')
def view_book(book_id):
    from models.book import Book
    book = Book.query.get_or_404(book_id)
    return render_template('book.html', book=book)
