"""
Generate monthly receipts for all active clients.
This script should be run once per month (e.g., via cron job or task scheduler).

Usage: python generate_monthly_receipts.py
"""

import sys
sys.path.insert(0, '/'.join(__file__.split('/')[:-2]))

from database import db, Client, Receipt
from app import app
from datetime import datetime
from number_to_words import number_to_words

def format_amount_in_letters(amount):
    """Convert numeric amount to French words"""
    try:
        # Split into euros and cents
        euros = int(amount)
        cents = round((amount - euros) * 100)
        
        euro_words = number_to_words(euros, lang='fr')
        
        if cents > 0:
            cent_words = number_to_words(cents, lang='fr')
            return f"{euro_words.capitalize()} euros et {cent_words} centimes"
        else:
            return f"{euro_words.capitalize()} euros"
    except Exception as e:
        return f"{amount:.2f} FCFA"

def generate_monthly_receipts():
    """Generate receipts for all active clients with monthly payments"""
    
    with app.app_context():
        # Get all active clients with monthly payments
        active_clients = Client.query.filter(
            Client.status == 'active',
            Client.monthly_payment > 0
        ).all()
        
        if not active_clients:
            print("✓ No active clients with monthly payments")
            return
        
        created_count = 0
        skipped_count = 0
        
        for client in active_clients:
            # Check if receipt already exists for this month
            current_month_start = datetime.now().replace(day=1)
            current_month_end = datetime.now()
            
            existing_receipt = Receipt.query.filter(
                Receipt.client_id == client.id,
                Receipt.date >= current_month_start,
                Receipt.date <= current_month_end
            ).first()
            
            if existing_receipt:
                print(f"⊘ Receipt already exists for {client.name} this month")
                skipped_count += 1
                continue
            
            try:
                # Generate receipt for monthly payment
                receipt_number = f"REC-{int(datetime.now().timestamp())}-{client.id}"
                amount_in_letters = format_amount_in_letters(client.monthly_payment)
                
                new_receipt = Receipt(
                    receipt_number=receipt_number,
                    customer_name=client.name,
                    description=f"Paiement mensuel - {client.name}",
                    payment_type='recurring_monthly',
                    price=client.monthly_payment,
                    amount_in_letters=amount_in_letters,
                    date=datetime.now(),
                    client_id=client.id
                )
                
                db.session.add(new_receipt)
                print(f"✓ Created receipt for {client.name}: {receipt_number}")
                created_count += 1
                
            except Exception as e:
                print(f"✗ Error creating receipt for {client.name}: {str(e)}")
                db.session.rollback()
        
        try:
            db.session.commit()
            print(f"\n✓ Monthly receipt generation complete!")
            print(f"  - Created: {created_count}")
            print(f"  - Skipped: {skipped_count}")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error committing changes: {str(e)}")
            return False
    
    return True

if __name__ == '__main__':
    print("Generating monthly receipts...\n")
    success = generate_monthly_receipts()
    sys.exit(0 if success else 1)
