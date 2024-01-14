from flask import Flask, request, jsonify
from passlib.hash import bcrypt
from uuid import uuid4
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import create_engine, text
from decouple import config
import json
from sqlalchemy.exc import IntegrityError
import re
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq', start=1000), primary_key=True)
    username = Column(String, unique=True) 
    email = Column(String, unique=True)
    password = Column(String)
    token = Column(String)

app = Flask(__name__)
swaggerui_blueprint = get_swaggerui_blueprint('/docs', '/static/swagger.json')
app.register_blueprint(swaggerui_blueprint, url_prefix='/docs')

DATABASE = config('DATABASE_PATH', default='./users3.db')
engine = create_engine('sqlite:///' + DATABASE, pool_recycle=3600)

Session = sessionmaker(bind=engine)
session = Session()

# Decorator for token validation
def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'status': 'fail', 'message': 'Authentication token is required'}), 401
        user = session.query(User).filter_by(token=token).first()
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

    password = bcrypt.hash(password)

    new_user = User(username=username, email=email, password=password)
    session.add(new_user)
    try:
        session.commit()
    except IntegrityError:
        return jsonify({'status': 'fail', 'message': 'Username or email already in use'}), 409
    except Exception as e:
        return jsonify({'status': 'fail', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': 'User registered successfully'}), 201

@app.route('/v1/account/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = session.query(User).filter_by(username=username).first()

    if user and bcrypt.verify(password, user.password):
        token = str(uuid4())
        user.token = token
        session.commit()
        return jsonify({'status': 'success', 'message': 'User logged in successfully', 'token': token}), 200
    else:
        return jsonify({'status': 'fail', 'message': 'Invalid username or password'}), 401

@app.route('/v1/account/profile', methods=['GET'])
@token_required
def profile(user):
    return jsonify({'username': user.username, 'email': user.email}), 200

@app.route('/v1/account/update-profile', methods=['PATCH'])
@token_required
def update_profile(user):
    new_email = request.form['email']
    if not new_email:
        return jsonify({'status': 'fail', 'message': 'New email is required'}), 400

    user.email = new_email
    session.commit()
    return jsonify({'status': 'success', 'message': 'User profile updated successfully'}), 200

@app.route('/v1/account/logout', methods=['POST'])
@token_required
def logout(user):
    user.token = None
    session.commit()
    return jsonify({'status': 'success', 'message': 'User logged out successfully'}), 200

@app.route('/v1/account/delete', methods=['DELETE'])
@token_required
def delete_account(user):
    session.delete(user)
    session.commit()
    return jsonify({'status': 'success', 'message': 'User account deleted successfully'}), 200

@app.route('/v1/account/list', methods=['GET'])
@token_required
def list_users(user):
    users = session.query(User).all()
    users_dict = [{'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_dict), 200

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run(host='0.0.0.0', port=int(config('PORT', default=5000)), debug=config('DEBUG_MODE', default=True, cast=bool))
