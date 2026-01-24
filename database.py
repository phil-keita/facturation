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
    Can also be linked to a Client for automatic monthly billing.
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
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=True, index=True)
    
    user = db.relationship('User', backref='receipts')
    client = db.relationship('Client', backref='receipts')
    
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


class Client(db.Model):
    """
    Client model for tracking clients and their service lifecycle.
    
    Status progression:
    - 'Conversation': Initial contact, minimal info (name, type, address only)
    - 'active': Working with client, full info (start_date, monthly_payment, installation_fee)
    - 'inactive': Stopped working with client
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    type = db.Column(db.String(100))  # e.g., "Cabinet dentaire", "Cabinet médical"
    address = db.Column(db.String(500))
    start_date = db.Column(db.Date, nullable=True)  # Null for "Conversation" status clients
    installation_fee = db.Column(db.Float, default=0.0)
    monthly_payment = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(50), default='Conversation')  # "Conversation", "active", "inactive"
    end_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Client {self.name}>'
