from utils.database import db
import json

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'created_at': self.created_at,
            'is_paid': self.is_paid
        })