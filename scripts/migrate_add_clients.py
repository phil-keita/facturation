"""
Migration script to add the Client table to existing databases.

Run this script once after deploying the new code with Client model.
It will create the client table without affecting existing data.

Usage:
    python scripts/migrate_add_clients.py
"""

import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from database import Client

def migrate():
    """Create the Client table if it doesn't exist."""
    with app.app_context():
        # This will create only the Client table if it doesn't exist
        # without affecting existing tables
        db.create_all()
        print("✓ Migration complete: Client table created successfully")
        
        # Show current client count
        client_count = Client.query.count()
        print(f"✓ Current number of clients in database: {client_count}")

if __name__ == '__main__':
    print("Starting migration to add Client table...")
    migrate()
    print("Migration finished!")
