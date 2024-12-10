import math

from sqlalchemy import text
from app.model.Config import Config
from app.model.Book import Book
from app import db
from app.model.BookGerne import BookGerne


def search_book(keyword=None, min_price=None, max_price=None,
               order=None, gerne_id=None, limit=None, page=None, quantity_status=None):
    query = Book.query
    if keyword:
        query = query.filter(Book.title.contains(keyword))
    if max_price:
        query = query.filter(Book.price.between(min_price, max_price))
    if order:
        if order == 'desc':
            query = query.order_by(Book.price.desc())
        elif order == 'asc':
            query = query.order_by(Book.price.asc())
    if gerne_id:
        gerne = BookGerne.query.get(gerne_id)
        query = query.join(BookGerne)
        query = query.filter(BookGerne.lft.between(gerne.lft, gerne.rgt))
    if quantity_status == 1:
        query = query.filter(Book.quantity >= Config.min_restock_level)
    elif quantity_status == 2:
        query = query.filter(Book.quantity < Config.min_restock_level)

    start = (page - 1) * limit
    end = start + limit
    query_count = query
    total = query_count.count()
    total_page = math.ceil(total / limit)
    query = query.slice(start, end)
    books = query.all()
    return {
        'total_book': total,
        'current_page': page,
        'pages': total_page,
        'books': books
    }
