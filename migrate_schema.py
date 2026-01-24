"""
Script to migrate the database schema and make start_date nullable.
This handles the SQLite limitation with ALTER TABLE by creating a new table
and migrating data.
"""

from app import app, db
from database import Client

def migrate_schema():
    """Migrate the database to make start_date nullable"""
    with app.app_context():
        try:
            # SQLite doesn't support modifying columns, so we need to recreate the table
            print("Starting migration...")
            
            # Get all existing clients
            existing_clients = Client.query.all()
            print(f"Found {len(existing_clients)} existing clients")
            
            # Back up client data
            clients_data = []
            for client in existing_clients:
                clients_data.append({
                    'name': client.name,
                    'type': client.type,
                    'address': client.address,
                    'start_date': client.start_date,
                    'installation_fee': client.installation_fee,
                    'monthly_payment': client.monthly_payment,
                    'status': client.status,
                    'end_date': client.end_date,
                    'created_at': client.created_at,
                })
            
            # Drop the old table
            Client.__table__.drop(db.engine)
            print("✓ Dropped old client table")
            
            # Create new table with updated schema
            Client.__table__.create(db.engine)
            print("✓ Created new client table with nullable start_date")
            
            # Restore data
            for data in clients_data:
                new_client = Client(**data)
                db.session.add(new_client)
            
            db.session.commit()
            print(f"✓ Restored {len(clients_data)} clients")
            print("✓ Migration completed successfully!")
            
        except Exception as e:
            print(f"✗ Migration failed: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_schema()
