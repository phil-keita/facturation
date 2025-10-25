from flask import Flask, render_template, request, send_file
from datetime import datetime
import os
from weasyprint import HTML

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/generate', methods=['POST'])
def generate_receipt():
    # Collect form data
    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    amount_in_letters = request.form['amount_in_letters']
    payment_type = request.form['payment_type']
    payment_reason = request.form.get('payment_reason', '')  # Optional field
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Generate receipt number (using timestamp for uniqueness)
    receipt_number = f"REC-{int(datetime.now().timestamp())}"

    # Render HTML receipt
    html = render_template('receipt_template.html', 
                         name=name, 
                         description=description, 
                         price=price, 
                         amount_in_letters=amount_in_letters,
                         payment_type=payment_type,
                         payment_reason=payment_reason,
                         date=date,
                         receipt_number=receipt_number)

    # Save and generate PDF
    if not os.path.exists('receipts'):
        os.makedirs('receipts')

    filename = f"receipt_{name}_{int(datetime.now().timestamp())}.pdf"
    pdf_path = os.path.join('receipts', filename)
    HTML(string=html).write_pdf(pdf_path)

    # Send PDF as a download
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
