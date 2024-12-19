from app.dao.OrderDAO import *
from app.dao.SearchDAO import search_book
from app.dao.FormImportDAO import get_form_imports
from app.dao.ConfigDAO import get_config
from flask import Blueprint
from datetime import datetime
import json
from app.model.User import UserRole
from app.model.User import User
from flask import jsonify
from flask import render_template, redirect, url_for, request
from flask_login import current_user

employee_bp = Blueprint('employee', __name__)


def employee_required(f):
    def wrap(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('account.employee_login'))
        if current_user.user_role not in [UserRole.EMPLOYEE_SALE, UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
                                          UserRole.EMPLOYEE_MANAGER]:
            return redirect(url_for('account.employee_login'))
        return f(*args, **kwargs)

    wrap.__name__ = f.__name__
    return wrap

@employee_bp.route("/checkout")
@employee_required
def checkout():
    books = search_book(limit=8, page=1)
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto

    return render_template("employee-checkout.html", books=books)


@employee_bp.route("/order")
@employee_required
def get_order():
    status = request.args.get("status")
    payment_method = request.args.get("paymentMethod")
    sort_by = request.args.get("sortBy")
    sort_dir = request.args.get("dir")
    order_type = request.args.get("orderType")
    page = request.args.get("page", 1)

    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")
    orders = find_all(status=status,
                      payment_method=payment_method,
                      sort_by=sort_by,
                      sort_dir=sort_dir,
                      order_type=order_type,
                      page=int(page),
                      start_date=start_date,
                      end_date=end_date)
    return render_template("employee-order.html", orders=orders, status=status, paymentMethod=payment_method,
                           sortBy=sort_by, sortDir=sort_dir, orderType=order_type)


@employee_bp.route("/order/<order_id>/update")
@employee_required
def update_order(order_id):
    order = find_by_id(order_id)

    books = searchBook(limit=8, page=1)
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict())
    books['books'] = book_dto
    return render_template("employee-order-update.html", order=order, books=books)


@employee_bp.route("/order/<order_id>/detail")
@employee_required
def get_order_detail(order_id):
    order = find_by_id(order_id)
    today = datetime.utcnow()
    return render_template("employee-order-detail.html", order=order, today=today)

@employee_bp.route("/category")
@employee_required
def get_category():
    with open('data/category.json', encoding="utf8") as f:
        data = json.load(f)
        categories = data[0:4]
    return categories


@employee_bp.route("/import")
@employee_required
def import_book():
    books = searchBook(limit=15, page=1)
    book_dto = []
    for book in books['books']:
        book_dto.append(book.to_dict_manage())
    books['books'] = book_dto
    config = get_config()
    return render_template("employee-import.html", books=books, config=config)


@employee_bp.route("/import/history")
@employee_required
def import_book_history():

    form_imports = get_form_imports()
    form_imports['form_imports'] = [form_import.to_dict() for form_import in form_imports['form_imports']]

    return render_template("employee-import-history.html", form_imports=form_imports)


# @employee_bp.route("/api/user_roles", methods=["GET"])
# def get_user_roles():
#     try:
#         employee_roles = [
#             UserRole.EMPLOYEE_SALE,
#             UserRole.EMPLOYEE_MANAGER_WAREHOUSE,
#             UserRole.EMPLOYEE_MANAGER,
#         ]
#         result = [{"user_role": role.name, "role_id": role.value} for role in employee_roles]
#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

