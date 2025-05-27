from flask import Blueprint, request, jsonify
from utils.database import db
from models.Users import User
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
from flask import current_app, make_response

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active
    }), 200

@user_blueprint.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_active': user.is_active
    } for user in users]), 200

@user_blueprint.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully!'}), 201

@user_blueprint.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.username = data['username']
    user.email = data['email']
    user.password = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'}), 200

@user_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not check_password_hash(user.password, data.get('password')):
        return jsonify({'message': 'Invalid credentials'}), 401
    token = jwt.encode({'user_id': user.id}, current_app.config['SECRET_KEY'], algorithm='HS256')
    resp = make_response(jsonify({'token': token}))
    resp.set_cookie('token', token, httponly=True)
    return resp, 200

@user_blueprint.route('/logout', methods=['POST'])
def logout():
    json_data = request.get_json(silent=True)
    token = request.cookies.get('token') or request.headers.get('Authorization') or (json_data.get('token') if json_data else None)
    if not token:
        return jsonify({'message': 'Token required for logout'}), 400
    resp = make_response(jsonify({'message': 'Logged out successfully!'}))
    resp.delete_cookie('token')
    return resp, 200

# verify token
@user_blueprint.route('/verify', methods=['GET'])
def verify_token():
    token = request.cookies.get('token') or request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing!'}), 401
    if token.startswith('Bearer '):
        token = token.split(' ')[1]
    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        return jsonify({'message': 'Token is valid', 'user_id': user.id}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token!'}), 401

@user_blueprint.route('/health', methods=['GET'])
def health():
    return '', 200