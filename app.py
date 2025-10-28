from flask import Flask, render_template, request, send_file, redirect, url_for
from datetime import datetime
import os
from weasyprint import HTML
from database import db, Receipt, Expense
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_receipt():
    # Collect form data
    name = request.form['name']
    payment_type = request.form['payment_type']
    payment_reason = request.form.get('payment_reason', '')  # Optional field for one_time
    
    # Set description based on payment type
    if payment_type == 'recurring_monthly':
        description = 'Paiement mensuel récurrent'
    else:
        description = payment_reason if payment_reason else 'Paiement unique'
    
    price = float(request.form['price'])
    amount_in_letters = request.form['amount_in_letters']
    date = datetime.now()
    
    # Generate receipt number (using timestamp for uniqueness)
    receipt_number = f"REC-{int(datetime.now().timestamp())}"
    
    # Save to database
    new_receipt = Receipt(
        receipt_number=receipt_number,
        customer_name=name,
        description=description,
        payment_type=payment_type,
        payment_reason=payment_reason,
        price=price,
        amount_in_letters=amount_in_letters,
        date=date
    )
    db.session.add(new_receipt)
    db.session.commit()

    # Render HTML receipt
    html = render_template('receipt_template.html', 
                         name=name, 
                         description=description, 
                         price=price, 
                         amount_in_letters=amount_in_letters,
                         payment_type=payment_type,
                         payment_reason=payment_reason,
                         date=date.strftime("%Y-%m-%d %H:%M:%S"),
                         receipt_number=receipt_number)

    # Save and generate PDF
    if not os.path.exists('receipts'):
        os.makedirs('receipts')

    filename = f"receipt_{name}_{int(datetime.now().timestamp())}.pdf"
    pdf_path = os.path.join('receipts', filename)
    HTML(string=html).write_pdf(pdf_path)

    # Send PDF as a download
    return send_file(pdf_path, as_attachment=True)

@app.route('/expenses', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        new_expense = Expense(description=description, amount=amount, date=datetime.now())
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')

@app.route('/dashboard')
def dashboard():
    # Totals
    total_income = db.session.query(func.sum(Receipt.price)).scalar() or 0
    total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
    net_income = total_income - total_expenses

    # Monthly income breakdown
    monthly_income_query = (
        db.session.query(
            func.strftime("%Y-%m", Receipt.date).label("month"),
            func.sum(Receipt.price).label("income")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    monthly_income_data = [(row.month, float(row.income)) for row in monthly_income_query]
    
    # Monthly expenses breakdown
    monthly_expenses_query = (
        db.session.query(
            func.strftime("%Y-%m", Expense.date).label("month"),
            func.sum(Expense.amount).label("expenses")
        )
        .group_by("month")
        .order_by("month")
        .all()
    )
    monthly_expenses_data = {row.month: float(row.expenses) for row in monthly_expenses_query}
    
    # Calculate net income per month
    monthly_net_data = []
    for month, income in monthly_income_data:
        expenses = monthly_expenses_data.get(month, 0)
        monthly_net_data.append((month, income - expenses))
    
    # Recent receipts
    recent_receipts = Receipt.query.order_by(Receipt.date.desc()).limit(10).all()
    
    # Recent expenses
    recent_expenses = Expense.query.order_by(Expense.date.desc()).limit(10).all()

    return render_template(
        'dashboard.html',
        total_income=total_income,
        total_expenses=total_expenses,
        net_income=net_income,
        monthly_income_data=monthly_income_data,
        monthly_net_data=monthly_net_data,
        recent_receipts=recent_receipts,
        recent_expenses=recent_expenses
    )

if __name__ == '__main__':
    app.run(debug=True)
