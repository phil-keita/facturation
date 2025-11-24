"""
Migration script to add user_id columns to receipt and expense tables.

Usage:
    python scripts/migrate_add_user_id.py

This script will:
1. Add user_id column to receipt table (nullable)
2. Add user_id column to expense table (nullable)
3. Set existing records to NULL (can be updated manually later)
"""

import os
import sys

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db

def migrate():
    with app.app_context():
        try:
            # Check if we're using SQLite or Postgres
            engine = db.engine.name
            
            print(f"Database engine: {engine}")
            print("Adding user_id columns to receipt and expense tables...")
            
            # Add user_id to receipt table
            try:
                db.session.execute(db.text(
                    'ALTER TABLE receipt ADD COLUMN user_id INTEGER REFERENCES "user"(id)'
                ))
                print("✓ Added user_id column to receipt table")
            except Exception as e:
                print(f"Note: receipt.user_id might already exist: {e}")
            
            # Add user_id to expense table
            try:
                db.session.execute(db.text(
                    'ALTER TABLE expense ADD COLUMN user_id INTEGER REFERENCES "user"(id)'
                ))
                print("✓ Added user_id column to expense table")
            except Exception as e:
                print(f"Note: expense.user_id might already exist: {e}")
            
            db.session.commit()
            print("\n✅ Migration completed successfully!")
            print("\nNote: Existing receipts and expenses have user_id set to NULL.")
            print("New receipts and expenses will automatically be associated with the logged-in user.")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Migration failed: {e}")
            sys.exit(1)

if __name__ == '__main__':
    migrate()
