import math
from colorsys import rgb_to_hls

from flask import jsonify
from sqlalchemy import text

from app.elasticsearch.BookIndex import BookIndex
from app.model.Config import Config
from app.model.Book import Book
from app import db, es
from app.model.BookGerne import BookGerne


def search_book_es(keyword, min_price, max_price,
                   order, lft, rgt, limit, page):
    index_name = BookIndex.index_name
    query = {}
    if keyword:
        query = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {
                                        "match_phrase_prefix": {
                                            "description": {
                                                "max_expansions": 2,
                                                "query": keyword,
                                                "slop": 3
                                            }
                                        }
                                    }
                                    , {
                                        "match_phrase_prefix": {
                                            "author": {
                                                "query": keyword,
                                                "max_expansions": 5
                                            }
                                        }
                                    }
                                    , {
                                        "match_phrase_prefix": {
                                            "title": {
                                                "boost": 2.0,
                                                "max_expansions": 5,
                                                "query": keyword
                                            }

                                        }
                                    }
                                    , {
                                        "nested": {
                                            "path": "extended_books",
                                            "query": {
                                                "match": {
                                                    "extended_books.value": {
                                                        "query": keyword,
                                                        "fuzziness": "AUTO"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ],
                    "filter": [
                        {
                            "range": {
                                "price": {
                                    "gte": min_price,
                                    "lte": max_price
                                }
                            },
                        }
                        , {
                            "nested": {
                                "path": "book_gerne",
                                "query": {
                                    "range": {
                                        "book_gerne.lft": {
                                            "gte": lft,
                                            "lte": rgt
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [
                {order['field']: order['direction']}
            ],
            "from": page * limit,
            "size": limit,
            "track_total_hits": True,
            "_source": ['book_id', 'book_image', "title", "price", "extended_books"]
        }
    else:
        query = {
            "query": {
                'bool':{
                    'must':[
                        {
                            "match_all": {}
                        }
                    ],
                    "filter": [
                        {
                            "range": {
                                "price": {
                                    "gte": min_price,
                                    "lte": max_price
                                }
                            },
                        }
                        , {
                            "nested": {
                                "path": "book_gerne",
                                "query": {
                                    "range": {
                                        "book_gerne.lft": {
                                            "gte": lft,
                                            "lte": rgt
                                        }
                                    }
                                }
                            }
                        }
                    ]
                }

            },
            "sort": [
                {order['field']: order['direction']}
            ],

            "from": page * limit,
            "size": limit,
            "track_total_hits": True,
            "_source": ['book_id', 'book_image', "title", "price", "extended_books"]
        }
    try:
        response = es.search(index=index_name, body=query)

        return {
            'data': response['hits']['hits'],
            'total': response['hits']['total']['value'],
        }  # Return matching documents
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
