from flask import Blueprint, request, jsonify
from utils.database import db
from models.Payment import Payment
from flask import current_app
from functools import wraps
import requests

payment_blueprint = Blueprint('payment', __name__)

# Decorador para requerir autenticación JWT consultando el servicio de users
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        token = request.cookies.get('token')
        headers = {}
        if auth_header:
            headers['Authorization'] = auth_header
        elif token:
            headers['Authorization'] = f'Bearer {token}'
        else:
            return jsonify({'message': 'Token is missing!'}), 401
        
        verify_url = 'http://auth-service/verify'
        try:
            response = requests.get(verify_url, headers=headers, timeout=3)
            if response.status_code != 200:
                return jsonify({'message': 'Token is invalid!'}), 401
            user_id = response.json().get('user_id')
            if not user_id:
                return jsonify({'message': 'User ID not found in verify response!'}), 401
        except Exception as e:
            return jsonify({'message': 'Auth service unavailable!'}), 503
        return f(user_id=user_id, *args, **kwargs)
    return decorated

@payment_blueprint.route('/payment/<int:id>', methods=['GET'])
@token_required
def get_payment(id, user_id):
    payment = Payment.query.filter_by(id=id, user_id=user_id).first_or_404()
    return jsonify({
        'id': payment.id,
        'order_id': payment.order_id,
        'user_id': payment.user_id,
        'status': payment.status,
        'created_at': payment.created_at.isoformat(),
        'is_paid': payment.is_paid,
        'payment_method': payment.payment_method,
        'amount': payment.amount
    }), 200

@payment_blueprint.route('/payment', methods=['GET'])
@token_required
def get_all_payments(user_id):
    payments = Payment.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': p.id,
        'order_id': p.order_id,
        'user_id': p.user_id,
        'status': p.status,
        'created_at': p.created_at.isoformat(),
        'is_paid': p.is_paid,
        'payment_method': p.payment_method,
        'amount': p.amount
    } for p in payments]), 200

@payment_blueprint.route('/payment', methods=['POST'])
@token_required
def create_payment(user_id):
    data = request.get_json()
    new_payment = Payment(
        order_id=data['order_id'],
        user_id=user_id,
        status=data['status'],
        is_paid=data.get('is_paid', False),
        payment_method=data.get('payment_method'),
        amount=data['amount']
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Payment created successfully!'}), 201

@payment_blueprint.route('/payment/<int:id>', methods=['PUT'])
@token_required
def update_payment(id, user_id):
    data = request.get_json()
    payment = Payment.query.filter_by(id=id, user_id=user_id).first_or_404()
    payment.status = data['status']
    payment.is_paid = data.get('is_paid', payment.is_paid)
    payment.payment_method = data.get('payment_method', payment.payment_method)
    payment.amount = data['amount']
    db.session.commit()
    return jsonify({'message': 'Payment updated successfully!'}), 200

@payment_blueprint.route('/payment/<int:id>', methods=['DELETE'])
@token_required
def delete_payment(id, user_id):
    payment = Payment.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted successfully!'}), 200

@payment_blueprint.route('/health', methods=['GET'])
def health():
    return '', 200