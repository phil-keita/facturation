"""
Script to clear all clients from the database.
"""

from app import app, db
from database import Client

def clear_clients():
    """Delete all clients from the database."""
    with app.app_context():
        count = Client.query.count()
        Client.query.delete()
        db.session.commit()
        print(f"✓ Deleted {count} clients from the database")

if __name__ == '__main__':
    clear_clients()
