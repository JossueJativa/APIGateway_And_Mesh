from flask import Flask
from utils.database import db
import os

from controller import user_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

db.init_app(app)

app.register_blueprint(user_blueprint)

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')