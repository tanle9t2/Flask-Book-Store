import confluent_kafka
from elasticsearch import Elasticsearch
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from urllib.parse import quote
from flask_apscheduler import APScheduler
from dotenv import dotenv_values, load_dotenv
import cloudinary
from flask_login import LoginManager
from app.utils.helper import format_currency_filter, format_datetime_filter, format_date_VN
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
load_dotenv()
scheduler = APScheduler()

DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

ELASTIC_HOST = os.getenv("ELASTIC_HOST")
ELASTIC_PORT = int(os.getenv("ELASTIC_PORT"))

KAFKA1 = os.getenv("KAFKA1")
KAFKA2 = os.getenv("KAFKA2")
KAFKA3 = os.getenv("KAFKA3")
RETURN_URL = os.getenv("RETURN_URL")

app.secret_key = "8923yhr9fuwnsejksnpokff@$I_I@$)opfk"
# app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL % quote(DB_PASSWORD)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@127.0.0.1:3307/book_store' % quote('15122004')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config["VNPAY_URL"] = 'https://sandbox.vnpayment.vn/paymentv2/vpcpay.html'  # Use the sandbox URL for testing
app.config["VNPAY_TMN_CODE"] = 'MEBTRFP0'
app.config["VNPAY_HASH_SECRET"] = 'ILFTJ080X209IM562X1NKYTMZ70RLVJO'
app.config["VNPAY_RETURN_URL"] = RETURN_URL
app.config['KAFKA_BROKER'] = [KAFKA1, KAFKA2, KAFKA3]
app.config['KAFKA_TOPIC'] = ['dbs_.book_store.book', 'dbs_.book_store.extended_book', 'schema-changes.mysql']

es = Elasticsearch(
    hosts=[{'host': ELASTIC_HOST, 'port': ELASTIC_PORT, 'scheme': 'http'}],
    http_auth=('webserver-cluster', '15122004')
)

consumers = {
    topic: confluent_kafka.Consumer({
        'bootstrap.servers': ','.join(app.config['KAFKA_BROKER']),
        'group.id': 'my-group',
        'auto.offset.reset': 'earliest'
    }) for topic in app.config['KAFKA_TOPIC']
}

cloudinary.config(
    cloud_name="duk7gxwvc",
    api_key="653944787632934",
    api_secret="GY20iNSIGW6CdrY1s1cDGwMKrqY",
    secure=True
)

app.config['SQLALCHEMY_ECHO'] = True
app.config['PAGE_SIZE'] = 12
app.config['ORDER'] = 'desc'

app.config["ORDER_PAGE_SIZE"] = 12
app.config["IMPORT_PAGE_SIZE"] = 20
app.config["STATISTIC_FRE_PAGE_SIZE"] = 6
app.config["STATISTIC_REVEN_PAGE_SIZE"] = 5
app.config["BOOK_PAGE_SIZE"] = 7

db = SQLAlchemy(app=app)
login = LoginManager(app)

# Register the custom filter in Jinja2
app.jinja_env.filters['currency'] = format_currency_filter
app.jinja_env.filters['datetime'] = format_datetime_filter
app.jinja_env.filters['date'] = format_date_VN()
