from flask import Flask, request, jsonify
from uuid import uuid4
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
import os
import json

app = Flask(__name__)

DATABASE = './users.db'

# Function to get a database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Function to initialize the database
def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                email TEXT,
                password TEXT,
                token TEXT
            )
        ''')
        db.commit()

# Endpoint for user registration
@app.route('/account/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']

    password = request.form['password'].encode('utf-8')  # Encode the password before hashing

    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)

    db = get_db_connection()
    db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
               (username, email, hashed_password))  # Password hashing should be used here
    db.commit()
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

# Endpoint for user login
@app.route('/account/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    db = get_db_connection()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user and user['password'] == password:  # In real-world, hash comparison
        token = str(uuid4())
        db.execute('UPDATE users SET token = ? WHERE id = ?', (token, user['id']))
        db.commit()
        return jsonify({'status': 'success', 'message': 'User logged in successfully', 'token': token}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid username or password'}), 401

# Endpoint for user profile
@app.route('/account/profile', methods=['GET'])
def profile():
    token = request.headers.get('Authorization')  # Token provided in the header
    db = get_db_connection()
    user = db.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()
    if user:
        return jsonify({'username': user['username'], 'email': user['email']})
    return jsonify({'status': 'fail', 'message': 'Invalid or expired session token'}), 401

# Endpoint to update user profile
@app.route('/account/update-profile', methods=['PATCH'])
def update_profile():
    token = request.headers.get('Authorization')  # Token provided in the header
    new_email = request.form['email']
    
    if not token:
        return jsonify({'status': 'fail', 'message': 'Authentication token is required'}), 401
    
    db = get_db_connection()
    user = db.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()
    
    if user:
        db.execute('UPDATE users SET email = ? WHERE id = ?', (new_email, user['id']))
        db.commit()
        return jsonify({'status': 'success', 'message': 'User profile updated successfully'})
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid or expired session token'}), 401


# Endpoint for user logout
@app.route('/account/logout', methods=['GET'])
def logout():
    token = request.headers.get('Authorization')
    db = get_db_connection()
    db.execute('UPDATE users SET token = NULL WHERE token = ?', (token,))
    db.commit()
    return jsonify({'status': 'success', 'message': 'User logged out successfully'})

# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = 'http://127.0.0.1:5000/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))

# Initialize the database
init_db()

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
