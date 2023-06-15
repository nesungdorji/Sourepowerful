from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Define a dictionary to store user credentials (replace with a database in a real-world scenario)
users = {
    'user1@example.com': 'password1',
    'user2@example.com': 'password2'
}

# Define a dictionary to store user tokens for verification
verification_tokens = {}

# Route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email in users and users[email] == password:
            session['email'] = email  # Store user's email in the session
            return redirect('/home')
        else:
            return 'Invalid login credentials'
    return render_template('login.html')

# Route for the home page
@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return redirect('/')

# Route for creating a new account
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users:
            return 'Account already exists for this email'
        
        # Generate a verification token
        verification_token = generate_verification_token()
        verification_tokens[email] = verification_token
        
        # Send verification email (placeholder)
        send_verification_email(email, verification_token)
        
        return 'Account created. Please check your email for verification.'
    
    return render_template('create_account.html')

# Route for verifying the email
@app.route('/verify_email', methods=['GET', 'POST'])
def verify_email():
    if request.method == 'POST':
        email = request.form['email']
        verification_code = request.form['verification_code']
        
        if email in verification_tokens and verification_code == verification_tokens[email]:
            # Add the user to the users dictionary
            password = request.form['password']
            users[email] = password
            
            # Clear the verification token
            del verification_tokens[email]
            
            return 'Email verified. Account created successfully.'
        
        return 'Invalid verification code'
    
    return render_template('verify_email.html')

# Helper function to generate a verification token
def generate_verification_token():
    # Generate a random 6-digit number as the token
    return str(random.randint(100000, 999999))

# Placeholder function for sending a verification email
def send_verification_email(email, verification_token):
    # In a real-world scenario, you would send an actual email with a link containing the verification_token
    print(f'Sending verification email to {email}. Token: {verification_token}')


@app.route('/purchase_record', methods=['GET', 'POST'])
def purchase_record():
    if request.method == 'POST':
        item_count = int(request.form['item_count'])
        return render_template('purchase_record.html', item_count=item_count)
    return render_template('purchase_record.html')

@app.route('/calculate_profit', methods=['POST'])
def calculate_profit():
    items = []
    total_quantity = 0
    total_profit = 0
    for i in range(int(request.form['item_count'])):
        item_number = request.form['item_number_' + str(i)]
        item_description = request.form['item_description_' + str(i)]
        quantity = int(request.form['quantity_' + str(i)])
        unit = request.form['unit_' + str(i)]
        rate = float(request.form['rate_' + str(i)])
        purchase_amount = quantity * rate
        markup_percentage = float(request.form['markup_percentage_' + str(i)])
        price = rate * (1 + markup_percentage / 100)
        selling_amount = quantity * price
        profit = selling_amount - purchase_amount
        items.append({
            'item_number': item_number,
            'item_description': item_description,
            'quantity': quantity,
            'unit': unit,
            'rate': rate,
            'purchase_amount': purchase_amount,
            'markup_percentage': markup_percentage,
            'price': price,
            'selling_amount': selling_amount,
            'profit': profit
        })
        total_quantity += quantity
        total_profit += profit

    return render_template('result.html', items=items, total_quantity=total_quantity, total_profit=total_profit)

if __name__ == '__main__':
    app.run(debug=True)
