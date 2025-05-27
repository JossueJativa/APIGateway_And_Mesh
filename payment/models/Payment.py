from utils.database import db
import json

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    is_paid = db.Column(db.Boolean, default=False)
    payment_method = db.Column(db.String(50), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'order_id': self.order_id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'is_paid': self.is_paid,
            'payment_method': self.payment_method,
            'amount': self.amount
        })