"""
Database models for the Marate AI Financial Management System.

This module defines SQLAlchemy models for:
- Users: Authentication and user management
- Receipts: Generated PDF receipts with automatic numbering
- Expenses: Expense tracking with user association
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    """
    User model for authentication and ownership tracking.
    
    The admin user is automatically created on first run with username='admin'.
    All receipts and expenses are associated with a user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Receipt(db.Model):
    """
    Receipt model for generated PDF receipts.
    
    Each receipt has a unique number and is associated with the user who created it.
    Supports recurring monthly payments and one-time payments with custom reasons.
    """
    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    payment_type = db.Column(db.String(50), nullable=False)  # 'recurring_monthly' or 'one_time'
    payment_reason = db.Column(db.String(200))  # Optional, for one-time payments
    price = db.Column(db.Float, nullable=False)
    amount_in_letters = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    
    user = db.relationship('User', backref='receipts')
    
    def __repr__(self):
        return f'<Receipt {self.receipt_number}>'


class Expense(db.Model):
    """
    Expense model for tracking business expenses.
    
    Each expense is associated with the user who created it.
    Used for calculating net income in the dashboard.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, index=True)
    
    user = db.relationship('User', backref='expenses')
    
    def __repr__(self):
        return f'<Expense {self.description}: {self.amount}>'
