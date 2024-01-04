from flask import Flask, request, jsonify
import bcrypt
from uuid import uuid4
from flask_swagger_ui import get_swaggerui_blueprint
import sqlite3
import os
import json

app = Flask(__name__)

DATABASE = os.getenv('DATABASE_PATH', './users.db')
app.config['DATABASE_POOL'] = None

# Function to start a connection pool
def create_db_pool():
    if app.config['DATABASE_POOL'] is None:
        conn = sqlite3.connect(DATABASE, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        app.config['DATABASE_POOL'] = conn
    return app.config['DATABASE_POOL']

# Decorator for token validation
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'fail', 'message': 'Authentication token is required'}), 401
        db = create_db_pool()
        user = db.execute('SELECT * FROM users WHERE token = ?', (token,)).fetchone()
        if not user:
            return jsonify({'status': 'fail', 'message': 'Invalid or expired session token'}), 401
        return f(user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/v1/account/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password'].encode('utf-8')

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt).decode('utf-8')

    db = create_db_pool()
    try:
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (username, email, hashed_password))
        db.commit()
    except sqlite3.IntegrityError as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 400
        
    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

@app.route('/v1/account/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    db = create_db_pool()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    if user and bcrypt.checkpw(password, user['password'].encode('utf-8')):
        token = str(uuid4())
        db.execute('UPDATE users SET token = ? WHERE id = ?', (token, user['id']))
        db.commit()
        return jsonify({'status': 'success', 'message': 'User logged in successfully', 'token': token}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid username or password'}), 401

@app.route('/v1/account/profile', methods=['GET'])
@token_required
def profile(user):
    return jsonify({'username': user['username'], 'email': user['email']}), 200

@app.route('/v1/account/update-profile', methods=['PATCH'])
@token_required
def update_profile(user):
    new_email = request.form['email']
    if not new_email:
        return jsonify({'status': 'fail', 'message': 'New email is required'}), 401
    
    db = create_db_pool()
    db.execute('UPDATE users SET email = ? WHERE id = ?', (new_email, user['id']))
    db.commit()
    return jsonify({'status': 'success', 'message': 'User profile updated successfully'}), 200

@app.route('/v1/account/logout', methods=['POST'])
@token_required
def logout(user):
    db = create_db_pool()
    db.execute('UPDATE users SET token = NULL WHERE id = ?', (user['id'],))
    db.commit()
    return jsonify({'status': 'success', 'message': 'User logged out successfully'}), 200

@app.route('/v1/account/delete', methods=['DELETE'])
@token_required
def delete_account(user):
    db = create_db_pool()
    db.execute('DELETE FROM users WHERE id = ?', (user['id'],))
    db.commit()
    return jsonify({'status': 'success', 'message': 'User account deleted successfully'}), 200

@app.route('/swagger.json')
def swagger():
    try:
        with open('swagger.json', 'r') as f:
            return jsonify(json.load(f))
    except (IOError, json.JSONDecodeError) as e:
        return jsonify({'status': 'fail', 'message': 'Unable to load swagger file: ' + str(e)}), 500

SWAGGER_URL = '/swagger'
API_URL = os.getenv('SWAGGER_API_URL', 'http://127.0.0.1:5000/swagger.json')
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Sample API"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=os.getenv('DEBUG_MODE', True))
