from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import os
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

    # Ensure an initial admin user exists (username 'admin', password 'admin')
    try:
        from database import User
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin_user = User(username='admin', password_hash=generate_password_hash('admin'))
            db.session.add(admin_user)
            db.session.commit()
            print("Created initial admin user with username 'admin' and password 'admin'")
    except Exception:
        # If DB not ready or other error, ignore here; app will create on demand
        pass

from database import User


# Simple session-based auth using the users table
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
    # Determine next URL precedence: form -> query arg -> default
    form_next = request.form.get('next') if request.method == 'POST' else None
    arg_next = request.args.get('next')
    next_url = form_next or arg_next or None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            session['username'] = username
            # If a next_url was provided and is valid, honor it. Otherwise, admins land on the admin UI.
            if next_url and next_url != 'None':
                return redirect(next_url)
            if username == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('index'))
        else:
            flash('Identifiants invalides', 'danger')
            return render_template('login.html', next=next_url), 401
    return render_template('login.html', next=next_url)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Serve a login form at /admin for unauthenticated users so the URL stays clean.
    # If a POST is received here, attempt login; only the admin user may access management.
    if request.method == 'POST' and not (session.get('logged_in') and session.get('username') == 'admin'):
        # Handle login attempt posted to /admin (only when not already logged-in as admin)
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['logged_in'] = True
            session['username'] = username
            flash('Connexion réussie.', 'success')
            # Only allow admin user onto the admin UI
            if username != 'admin':
                flash('Accès administrateur requis', 'danger')
                return redirect(url_for('index'))
            # Redirect after successful login to avoid treating this POST as a create-user action
            return redirect(url_for('admin'))
        else:
            flash('Identifiants invalides', 'danger')
            # fall through to render login form again (still at /admin)

    # If the user is not logged in or not admin, show login form (but keep URL /admin)
    if not session.get('logged_in') or session.get('username') != 'admin':
        return render_template('login.html', next='/admin', action_url=url_for('admin'))

    # At this point user is logged in as admin and can manage users
    if request.method == 'POST' and (session.get('logged_in') and session.get('username') == 'admin'):
        # This block handles creating users when an authenticated admin posts the create form
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Le nom d\'utilisateur et le mot de passe sont requis', 'danger')
        else:
            if User.query.filter_by(username=username).first():
                flash('L\'utilisateur existe déjà', 'danger')
            else:
                new_user = User(username=username, password_hash=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                flash(f'Utilisateur {username} créé', 'success')

    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin.html', users=users)


@app.route('/admin/delete', methods=['POST'])
@login_required
def admin_delete():
    # Only admin username may perform deletions
    if session.get('username') != 'admin':
        flash('Accès administrateur requis', 'danger')
        return redirect(url_for('index'))

    user_id = request.form.get('user_id')
    if not user_id:
        flash('ID utilisateur manquant', 'danger')
        return redirect(url_for('admin'))

    user = User.query.get(user_id)
    if not user:
        flash('Utilisateur introuvable', 'danger')
        return redirect(url_for('admin'))

    if user.username == 'admin':
        flash('Impossible de supprimer le compte administrateur', 'danger')
        return redirect(url_for('admin'))

    db.session.delete(user)
    db.session.commit()
    flash(f'Utilisateur {user.username} supprimé', 'success')
    return redirect(url_for('admin'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    user = User.query.filter_by(username=session.get('username')).first()
    if not user:
        flash('Utilisateur introuvable', 'danger')
        return redirect(url_for('logout'))

    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'update_username':
            new_username = request.form.get('new_username', '').strip()
            if not new_username:
                flash('Le nom d\'utilisateur ne peut pas être vide', 'danger')
            elif new_username != user.username and User.query.filter_by(username=new_username).first():
                flash('Nom d\'utilisateur déjà utilisé', 'danger')
            else:
                user.username = new_username
                session['username'] = new_username
                db.session.commit()
                flash('Nom d\'utilisateur mis à jour avec succès', 'success')
        
        elif action == 'update_password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')
            
            if not check_password_hash(user.password_hash, current_password):
                flash('Le mot de passe actuel est incorrect', 'danger')
            elif not new_password or len(new_password) < 4:
                flash('Le nouveau mot de passe doit contenir au moins 4 caractères', 'danger')
            elif new_password != confirm_password:
                flash('Les nouveaux mots de passe ne correspondent pas', 'danger')
            else:
                user.password_hash = generate_password_hash(new_password)
                db.session.commit()
                flash('Mot de passe mis à jour avec succès', 'success')
        
        return redirect(url_for('account'))
    
    return render_template('account.html', user=user)

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
    
    # Get current user
    current_user = User.query.filter_by(username=session.get('username')).first()
    
    # Save to database
    new_receipt = Receipt(
        receipt_number=receipt_number,
        customer_name=name,
        description=description,
        payment_type=payment_type,
        payment_reason=payment_reason,
        price=price,
        amount_in_letters=amount_in_letters,
        date=date,
        user_id=current_user.id if current_user else None
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
    # Try to generate a PDF using WeasyPrint. If the native dependencies are
    # missing (common on Windows), gracefully fall back to returning the
    # rendered HTML so you can still test the UI without installing GTK.
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(pdf_path)
        return send_file(pdf_path, as_attachment=True)
    except Exception as e:
        # Log to console for developer visibility and return HTML fallback
        print("WeasyPrint PDF generation failed:", e)
        flash('La génération PDF n\'est pas disponible dans cet environnement. Affichage HTML de secours.', 'warning')
        return html, 200, {'Content-Type': 'text/html'}

@app.route('/expenses', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = float(request.form['amount'])
        current_user = User.query.filter_by(username=session.get('username')).first()
        new_expense = Expense(
            description=description, 
            amount=amount, 
            date=datetime.now(),
            user_id=current_user.id if current_user else None
        )
        db.session.add(new_expense)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get current user
    current_user = User.query.filter_by(username=session.get('username')).first()
    
    # Check if user wants to see company-wide data (default to personal)
    view_mode = request.args.get('view', 'personal')  # 'personal' or 'company'
    
    # Build queries based on view mode
    if view_mode == 'company':
        # Company-wide data (no user filter)
        receipts_query = Receipt.query
        expenses_query = Expense.query
    else:
        # Personal data only (filter by current user)
        receipts_query = Receipt.query.filter_by(user_id=current_user.id if current_user else None)
        expenses_query = Expense.query.filter_by(user_id=current_user.id if current_user else None)
    
    # Totals
    total_income = db.session.query(func.sum(Receipt.price)).filter(
        Receipt.user_id == current_user.id if view_mode == 'personal' and current_user else True
    ).scalar() or 0
    
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id if view_mode == 'personal' and current_user else True
    ).scalar() or 0
    
    net_income = total_income - total_expenses

    # Dialect-neutral monthly aggregation
    receipts = receipts_query.with_entities(Receipt.date, Receipt.price).all()
    expenses_rows = expenses_query.with_entities(Expense.date, Expense.amount).all()

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
    
    # Recent receipts (don't show user info to maintain privacy)
    recent_receipts = receipts_query.order_by(Receipt.date.desc()).limit(10).all()
    
    # Recent expenses (don't show user info to maintain privacy)
    recent_expenses = expenses_query.order_by(Expense.date.desc()).limit(10).all()

    return render_template(
        'dashboard.html',
        total_income=total_income,
        total_expenses=total_expenses,
        net_income=net_income,
        monthly_income_data=monthly_income_data,
        monthly_net_data=monthly_net_data,
        recent_receipts=recent_receipts,
        recent_expenses=recent_expenses,
        view_mode=view_mode
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
