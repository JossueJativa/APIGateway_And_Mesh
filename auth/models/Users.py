from utils.database import db
import json

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return json.dumps({
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active
        })