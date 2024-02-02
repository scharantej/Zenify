
# Import necessary modules
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Create a Flask app
app = Flask(__name__)

# Database configuration
DATABASE = 'mindfulness_content.db'

def get_db():
    db = getattr(app, '_database', None)
    if db is None:
        db = app._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(app, '_database', None)
    if db is not None:
        db.close()

# Home page route
@app.route('/')
def index():
    return render_template('index.html')

# Sign up route
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    time = request.form['time']

    # Save user information to the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO users (name, email, time) VALUES (?, ?, ?)',
                   (name, email, time))
    db.commit()

    return redirect(url_for('confirmation'))

# Confirmation page route
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# Mindfulness content route
@app.route('/mindfulness_content')
def mindfulness_content():
    # Retrieve user information from the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # Generate mindfulness content
    content = 'Insert your mindfulness content here'

    # Send mindfulness content to users via email
    for user in users:
        send_email(user['email'], content)

    return 'Mindfulness content sent successfully'

# Unsubscribe route
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form['email']

    # Remove user from the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE email=?', (email,))
    db.commit()

    return 'Unsubscribed successfully'

# Function to send emails
def send_email(email, content):
    # Use a third-party email service to send the content
    # This is just a placeholder, you need to implement the actual email sending logic here
    print(f'Sending content to {email}')

# Main function
if __name__ == '__main__':
    app.run(debug=True)
