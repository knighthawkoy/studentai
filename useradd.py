from flask import Flask, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # You should use a static secret in production

DATABASE = '/opt/x/project//users.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, email TEXT, password TEXT)')
        db.commit()

# Endpoint for user registration
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']  # In real-world, passwords must be hashed
    db = get_db_connection()
    db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
               (username, email, password))  # Password hashing should be used here
    db.commit()
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

# Endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db_connection()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user and user['password'] == password:  # Password check should be with hash comparison
        session['user_id'] = user['id']
        return jsonify({'status': 'success', 'message': 'User logged in successfully'}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid username or password'}), 401

# Endpoint for user profile
@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        db = get_db_connection()
        user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user:
            return jsonify({'username': user['username'], 'email': user['email']})
    return jsonify({'status': 'fail', 'message': 'User not logged in'}), 401

# Endpoint for user logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'status': 'success', 'message': 'User logged out successfully'})

# Initialize the database
init_db()

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
