from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime

# Class User
# Represents the user of 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(length=100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(length=100), index=True, unique=True, nullable=False)
    password = db.Column(db.String(length=256), nullable=False)

    # Identity function
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # Setting password of user
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Checking if the password of user is correct    
    def check_password(self, password):
        print(password)
        print(self.password)
        print(generate_password_hash(password))
        return check_password_hash(self.password, password)
    
    # Generate auth token
    def generate_auth_token(self, expiration = 60):
        token = jwt.encode({'id': self.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration)}, app.config['SECRET_KEY'], "HS256")
        return token