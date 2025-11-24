"""
Database Population Script for Marate AI Financial Management System

This script generates realistic test data for development and testing:
- Creates 100+ receipts over 12 months with varied customers and amounts
- Generates 70+ expenses with different categories
- Useful for testing the dashboard, charts, and filtering features

⚠️ WARNING: This script DELETES all existing receipts and expenses!
Only use in development environments.

Usage:
    python populate_db.py
"""

from app import app, db
from database import Receipt, Expense
from datetime import datetime, timedelta
import random

def populate_database():
    with app.app_context():
        # Clear existing data (optional)
        print("Clearing existing data...")
        Receipt.query.delete()
        Expense.query.delete()
        db.session.commit()
        
        # Sample customer names
        customers = [
            "Entreprise Alpha SA",
            "Beta Solutions",
            "Gamma Tech",
            "Delta Services",
            "Epsilon Corp",
            "Zeta Industries",
            "Eta Consulting",
            "Theta Partners"
        ]
        
        # Sample descriptions for one-time payments
        one_time_reasons = [
            "Consultation stratégique",
            "Formation en ligne",
            "Développement de site web",
            "Maintenance serveur",
            "Configuration réseau",
            "Audit de sécurité",
            "Migration de données",
            "Support technique"
        ]
        
        # Sample expense descriptions
        expense_types = [
            "Fournitures de bureau",
            "Abonnement logiciel",
            "Hébergement web",
            "Électricité",
            "Internet",
            "Marketing digital",
            "Formation professionnelle",
            "Frais bancaires",
            "Location bureau",
            "Assurance"
        ]
        
        # Generate receipts for the last 12 months
        print("Generating receipts...")
        base_date = datetime.now()
        receipt_count = 0
        receipt_counter = 1
        
        for month_offset in range(12):
            # Generate 5-15 receipts per month
            num_receipts = random.randint(5, 15)
            
            for _ in range(num_receipts):
                # Random date within the month
                days_back = month_offset * 30 + random.randint(0, 29)
                receipt_date = base_date - timedelta(days=days_back)
                
                # Random customer
                customer = random.choice(customers)
                
                # Random payment type
                payment_type = random.choice(['recurring_monthly', 'one_time'])
                
                if payment_type == 'recurring_monthly':
                    description = "Abonnement mensuel - Services IA Marate"
                    payment_reason = None
                    price = random.choice([50000, 75000, 100000, 150000, 200000])
                else:
                    description = None
                    payment_reason = random.choice(one_time_reasons)
                    price = random.randint(25000, 500000)
                
                # Amount in letters (simplified)
                amount_letters = f"{price:,} Francs CFA".replace(',', ' ')
                
                # Generate unique receipt number with counter
                receipt = Receipt(
                    receipt_number=f"REC-{int(receipt_date.timestamp())}-{receipt_counter}",
                    customer_name=customer,
                    description=description,
                    payment_type=payment_type,
                    payment_reason=payment_reason,
                    price=price,
                    amount_in_letters=amount_letters,
                    date=receipt_date
                )
                
                db.session.add(receipt)
                receipt_count += 1
                receipt_counter += 1
        
        print(f"Generated {receipt_count} receipts")
        
        # Generate expenses for the last 12 months
        print("Generating expenses...")
        expense_count = 0
        
        for month_offset in range(12):
            # Generate 3-8 expenses per month
            num_expenses = random.randint(3, 8)
            
            for _ in range(num_expenses):
                # Random date within the month
                days_back = month_offset * 30 + random.randint(0, 29)
                expense_date = base_date - timedelta(days=days_back)
                
                # Random expense type
                expense_desc = random.choice(expense_types)
                
                # Random amount based on expense type
                if expense_desc in ["Fournitures de bureau", "Frais bancaires"]:
                    amount = random.randint(5000, 25000)
                elif expense_desc in ["Abonnement logiciel", "Hébergement web", "Internet"]:
                    amount = random.randint(10000, 50000)
                elif expense_desc in ["Location bureau", "Marketing digital"]:
                    amount = random.randint(50000, 150000)
                else:
                    amount = random.randint(15000, 75000)
                
                expense = Expense(
                    description=expense_desc,
                    amount=amount,
                    date=expense_date
                )
                
                db.session.add(expense)
                expense_count += 1
        
        print(f"Generated {expense_count} expenses")
        
        # Commit all changes
        db.session.commit()
        print("Database populated successfully!")
        
        # Print summary
        total_income = db.session.query(db.func.sum(Receipt.price)).scalar() or 0
        total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
        print(f"\nSummary:")
        print(f"Total Receipts: {receipt_count}")
        print(f"Total Income: {total_income:,.0f} FCFA")
        print(f"Total Expenses: {expense_count}")
        print(f"Total Expense Amount: {total_expenses:,.0f} FCFA")
        print(f"Net Income: {(total_income - total_expenses):,.0f} FCFA")

if __name__ == "__main__":
    populate_database()
