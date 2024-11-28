from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
from app.utils.helper import format_currency_filter

app = Flask(__name__)
app.secret_key = "8923yhr9fuwnsejksnpok@$I_I@$)opfk"
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:090224T%40n@localhost/book_store'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["VNPAY_URL"] = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # Use the sandbox URL for testing
app.config["VNPAY_TMN_CODE"] = 'MEBTRFP0'
app.config["VNPAY_HASH_SECRET"] = 'XGR3PAJ4STE368KZBJQ2GO2KJBS1R6HF'
app.config["VNPAY_RETURN_URL"] = 'http://127.0.0.1:5000/api/v1/payment/return'

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] = 12
app.config['ORDER'] = 'desc'

app.config["ORDER_PAGE_SIZE"] = 6

db = SQLAlchemy(app=app)
login = LoginManager(app)
# Register the custom filter in Jinja2
app.jinja_env.filters['currency'] = format_currency_filter
app.jinja_env.filters['datetime'] = format_datetime_filter
