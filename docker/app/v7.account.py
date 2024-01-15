from flask import Flask, request, jsonify
from passlib.hash import bcrypt
from uuid import uuid4
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import create_engine, text
from decouple import config
import json
from sqlalchemy.exc import IntegrityError
import re

app = Flask(__name__)
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/swagger.json')
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

DATABASE = config('DATABASE_PATH', default='./users2.db')
engine = create_engine('sqlite:///' + DATABASE, pool_recycle=3600)


# Create table is not exists
def create_users_table():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                token TEXT
            )
        """))

# Function to get a connection
def get_db_connection():
    conn = engine.connect()
    conn.execution_options(isolation_level="AUTOCOMMIT")
    return conn
    


# Decorator for token validation
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'fail', 'message': 'Authentication token is required'}), 401
        conn = get_db_connection()
        user = conn.execute(text('SELECT * FROM users WHERE token = :token'), {'token': token}).fetchone()
        if not user:
            return jsonify({'status': 'fail', 'message': 'Invalid or expired session token'}), 401
        return f(user, *args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/v1/account/register', methods=['POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Validate input
    if not username or not email or not password:
        return jsonify({'status': 'fail', 'message': 'Username, email, and password are required'}), 400
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({'status': 'fail', 'message': 'Invalid email format'}), 400

  
    password = bcrypt.using(rounds=12).hash(password)

    conn = get_db_connection()
    try:
        conn.execute(text('INSERT INTO users (username, email, password) VALUES (:username, :email, :password)'),
                     {'username': username, 'email': email, 'password': password})
    except IntegrityError:
        return jsonify({'status': 'fail', 'message': 'Username or email already in use'}), 409
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

@app.route('/v1/account/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = get_db_connection()
    user = conn.execute(text('SELECT * FROM users WHERE username = :username'), {'username': username}).fetchone()

    if user and bcrypt.verify(password, user['password']):
        token = str(uuid4())
        conn.execute(text('UPDATE users SET token = :token WHERE id = :id'), {'token': token, 'id': user['id']})
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
    
    conn = get_db_connection()
    conn.execute(text('UPDATE users SET email = :email WHERE id = :id'), {'email': new_email, 'id': user['id']})
    return jsonify({'status': 'success', 'message': 'User profile updated successfully'}), 200

@app.route('/v1/account/logout', methods=['POST'])
@token_required
def logout(user):
    conn = get_db_connection()
    conn.execute(text('UPDATE users SET token = NULL WHERE id = :id'), {'id': user['id']})
    return jsonify({'status': 'success', 'message': 'User logged out successfully'}), 200

@app.route('/v1/account/delete', methods=['DELETE'])
@token_required
def delete_account(user):
    conn = get_db_connection()
    conn.execute(text('DELETE FROM users WHERE id = :id'), {'id': user['id']})
    return jsonify({'status': 'success', 'message': 'User account deleted successfully'}), 200

@app.route('/v1/account/list', methods=['GET'])
@token_required
def list_users(user):
    conn = get_db_connection()
    users = conn.execute(text('SELECT * FROM users')).fetchall()
    users_dict = [dict(user) for user in users]
    return jsonify({'users': users_dict}), 200

@app.route('/swagger.json')
def swagger():
    try:
        with open('swagger.json', 'r') as f:
            return jsonify(json.load(f))
    except (IOError, json.JSONDecodeError) as e:
       
        return jsonify({'status': 'fail', 'message': str(e)}), 500

@app.route('/docs', methods=['GET'])
def docs():
    return jsonify({'status': 'success', 'message': 'Swagger UI is available at /docs'}), 200

if __name__ == '__main__':
    create_users_table()
    app.run(host='0.0.0.0', port=int(config('PORT', default=5000)), debug=config('DEBUG_MODE', default=True, cast=bool))
    