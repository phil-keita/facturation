"""
Script to import clients from Excel file into the database.

Maps Excel columns to Client model fields.
Parses payment information from text strings.
"""

import re
from datetime import datetime
from app import app, db
from database import Client
import openpyxl

def parse_amount(text):
    """Extract numeric amount from text like '50k' or '10.000'."""
    if not text or text == 'None':
        return 0.0
    
    # Remove spaces and convert to string
    text = str(text).strip().lower()
    
    # Extract numbers
    match = re.search(r'(\d+\.?\d*)', text.replace('.', '').replace(',', '.'))
    if match:
        amount = float(match.group(1))
        # If 'k' is in text, multiply by 1000
        if 'k' in text:
            amount *= 1000
        return amount
    return 0.0

def import_clients():
    """Import clients from Excel file."""
    
    wb = openpyxl.load_workbook('Etat_conversation_Marate.xlsx')
    ws = wb.active
    
    imported = 0
    errors = []
    
    # Skip header row (row 1)
    for row_idx, row in enumerate(ws.iter_rows(min_row=2, values_only=True), 1):
        try:
            name = row[0]
            client_type = row[1]
            address = row[2]
            start_date = row[5]
            payment_info = row[6]
            status_raw = row[4] if row[4] else 'Conversation'
            
            # Map Excel status to database status
            status = status_raw.lower().strip()
            if status in ['livré', 'active', 'en cours de livraison']:
                status = 'active'
            elif status in ['en attente', 'conversation', 'pending']:
                status = 'Conversation'
            else:
                status = 'Conversation'
            
            # Skip empty rows
            if not name:
                continue
            
            # Clean up data
            name = str(name).strip()
            client_type = str(client_type).strip() if client_type else None
            address = str(address).strip() if address else None
            status = str(status).strip().lower()
            
            # Parse installation fee and monthly payment
            installation_fee = 0.0
            monthly_payment = 0.0
            
            if payment_info:
                payment_text = str(payment_info).lower()
                
                # Extract installation fee (usually "50k installation" or similar)
                if 'installation' in payment_text:
                    installation_fee = parse_amount(payment_text.split('installation')[0])
                
                # Extract monthly payment (usually "10k par mois" or similar)
                if 'mois' in payment_text or 'par mois' in payment_text:
                    # Get the last number before 'mois' or 'par mois'
                    monthly_part = payment_text.split('installation')[-1] if 'installation' in payment_text else payment_text
                    monthly_payment = parse_amount(monthly_part)
            
            # Handle start_date
            if isinstance(start_date, datetime):
                start_date = start_date.date()
            else:
                start_date = datetime.now().date()
            
            # Check if client already exists
            existing = Client.query.filter_by(name=name).first()
            if existing:
                print(f"⚠️  Row {row_idx}: Client '{name}' already exists, skipping")
                continue
            
            # Create client
            client = Client(
                name=name,
                type=client_type,
                address=address,
                start_date=start_date,
                installation_fee=installation_fee,
                monthly_payment=monthly_payment,
                status=status
            )
            
            db.session.add(client)
            imported += 1
            
            print(f"✓ Row {row_idx}: Imported '{name}'")
            print(f"  Type: {client_type}")
            print(f"  Address: {address}")
            print(f"  Start Date: {start_date}")
            print(f"  Installation Fee: {installation_fee} FCFA")
            print(f"  Monthly Payment: {monthly_payment} FCFA")
            print(f"  Status: {status}\n")
            
        except Exception as e:
            errors.append(f"Row {row_idx}: {str(e)}")
            print(f"✗ Row {row_idx}: Error - {str(e)}\n")
    
    # Commit all changes
    try:
        db.session.commit()
        print(f"\n{'='*60}")
        print(f"✓ Successfully imported {imported} clients")
        if errors:
            print(f"⚠️  {len(errors)} rows had errors:")
            for error in errors:
                print(f"  - {error}")
        print(f"{'='*60}")
    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error committing changes: {e}")

if __name__ == '__main__':
    with app.app_context():
        import_clients()
