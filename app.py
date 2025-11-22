from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from datetime import datetime
import os
from weasyprint import HTML
from database import db, Receipt, Expense
from sqlalchemy import func, text
import secrets

app = Flask(__name__)

# Secret key (use env or generate ephemeral for dev)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex(16)

# Database URL from env (Postgres in production) or fallback to local SQLite
database_url = os.getenv('DATABASE_URL') or 'sqlite:///data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# Simple session-based auth
# Credentials are read from environment: ADMIN_USER, ADMIN_PASSWORD
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'password')

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return decorated


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_url = request.args.get('next') or url_for('index')
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == ADMIN_USER and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash('Logged in successfully.', 'success')
            return redirect(next_url)
        else:
            flash('Invalid credentials', 'danger')
            return render_template('login.html', next=next_url), 401
    return render_template('login.html', next=next_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
@login_required
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
@login_required
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
@login_required
def dashboard():
    # Totals
    total_income = db.session.query(func.sum(Receipt.price)).scalar() or 0
    total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
    net_income = total_income - total_expenses

    # Dialect-neutral monthly aggregation (group in Python for simplicity and portability)
    receipts = db.session.query(Receipt.date, Receipt.price).all()
    expenses_rows = db.session.query(Expense.date, Expense.amount).all()

    income_by_month = {}
    for dt, price in receipts:
        key = dt.strftime('%Y-%m')
        income_by_month[key] = income_by_month.get(key, 0) + float(price)

    expenses_by_month = {}
    for dt, amount in expenses_rows:
        key = dt.strftime('%Y-%m')
        expenses_by_month[key] = expenses_by_month.get(key, 0) + float(amount)

    all_months = sorted(set(list(income_by_month.keys()) + list(expenses_by_month.keys())))
    monthly_income_data = [(m, income_by_month.get(m, 0)) for m in all_months]
    monthly_net_data = [(m, income_by_month.get(m, 0) - expenses_by_month.get(m, 0)) for m in all_months]
    
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

@app.route('/healthz')
def healthz():
    try:
        db_ok = db.session.execute(text('SELECT 1')).scalar() == 1
        return {'status': 'ok', 'db': db_ok}, 200
    except Exception as e:
        return {'status': 'error', 'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
