from sqlalchemy import Column, Integer, String, ForeignKey, Double
from app import db
from app.model.BookImage import ImageOfBook
from enum import Enum
from babel.numbers import format_currency
import functools
from datetime import datetime, timezone


class Status(Enum):
    LE = 1
    TAN = 2
    PHAT = 3

obj = {
    "name": "Phat",
    "age": 12
}

print(datetime.utcnow())
print(format_currency(120222, "VND", locale='vi_VN'))

# print(Status.LE.value.__eq__('1'))

# obj1 = {
#     'name': 'phat',
#     'age': 12
# }
#
# obj2 = [
#     {
#         'width': 2,
#         'height': 2
#     }, {
#         'width': 3,
#         'height': 3
#
#     }
# ]
#
# x = functools.reduce(lambda a, b: a['width'] * a['height'] + b['width'] * b['height'], obj2)
# print(x)