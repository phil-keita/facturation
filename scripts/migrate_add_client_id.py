"""
Migration script to add client_id field to Receipt model.
This allows linking receipts to clients for monthly billing.
"""

import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))

from database import db, Receipt, Client
from app import app
from sqlalchemy import text

with app.app_context():
    # Check if client_id column already exists
    inspector = db.inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns('receipt')]
    
    if 'client_id' in columns:
        print("✓ client_id column already exists in Receipt table")
        sys.exit(0)
    
    print("Adding client_id column to Receipt table...")
    
    try:
        # Add the new column (SQLite doesn't support foreign keys in ALTER, we'll add the column and handle FK in the model)
        with db.engine.connect() as connection:
            connection.execute(text("""
                ALTER TABLE receipt 
                ADD COLUMN client_id INTEGER
            """))
            connection.commit()
        
        print("✓ Successfully added client_id column to Receipt table")
        print("✓ Migration complete!")
        print("  Note: Foreign key constraint is defined in the SQLAlchemy model")
        
    except Exception as e:
        print(f"✗ Error during migration: {str(e)}")
        sys.exit(1)
