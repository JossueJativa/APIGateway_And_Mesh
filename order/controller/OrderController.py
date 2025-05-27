from flask import Blueprint, request, jsonify
from utils.database import db
from models.Orders import Order
import requests

order_blueprint = Blueprint('order', __name__)

def has_valid_payment(order_id, user_id, auth_header):
    payment_url = 'http://payment-service/payment'
    try:
        payment_response = requests.get(payment_url, headers={
            'Authorization': auth_header
        }, timeout=3)
        if payment_response.status_code != 200:
            return False, 'No valid payment found for user'
        payments = payment_response.json()
        for p in payments:
            if p['order_id'] == order_id and p['user_id'] == user_id:
                return True, None
        return False, 'No valid payment found for this order and user'
    except Exception:
        return False, 'Payment service unavailable!'

@order_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'status': order.status,\
        'created_at': order.created_at,
        'is_paid': order.is_paid
    }), 200

@order_blueprint.route('/orders', methods=['GET'])
def get_all_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'status': order.status,
        'created_at': order.created_at,
        'is_paid': order.is_paid
    } for order in orders]), 200

@order_blueprint.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data['user_id']
    new_order = Order(
        user_id=user_id,
        status=data['status'],
        is_paid=data.get('is_paid', False)
    )
    db.session.add(new_order)
    db.session.commit()
    ok, msg = has_valid_payment(new_order.id, user_id, request.headers.get('Authorization', ''))
    if not ok:
        db.session.delete(new_order)
        db.session.commit()
        return jsonify({'message': msg}), 403 if 'valid payment' in msg else 503
    return jsonify({'message': 'Order created successfully!'}), 201

@order_blueprint.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()
    order = Order.query.get_or_404(order_id)
    user_id = data.get('user_id', order.user_id)
    ok, msg = has_valid_payment(order_id, user_id, request.headers.get('Authorization', ''))
    if not ok:
        return jsonify({'message': msg}), 403 if 'valid payment' in msg else 503
    order.user_id = user_id
    order.status = data.get('status', order.status)
    order.is_paid = data.get('is_paid', order.is_paid)
    db.session.commit()
    return jsonify({'message': 'Order updated successfully!'}), 200

@order_blueprint.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    user_id = order.user_id
    ok, msg = has_valid_payment(order_id, user_id, request.headers.get('Authorization', ''))
    if not ok:
        return jsonify({'message': msg}), 403 if 'valid payment' in msg else 503
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted successfully!'}), 200

@order_blueprint.route('/health', methods=['GET'])
def health():
    return '', 200