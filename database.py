from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True)
    customer_name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    payment_type = db.Column(db.String(50))  # recurring_monthly or one_time
    payment_reason = db.Column(db.String(200))  # Optional, for one_time payments
    price = db.Column(db.Float)
    amount_in_letters = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.now)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.now)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
