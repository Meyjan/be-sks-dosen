from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
import datetime

# Class User
# Represents the user (usually a lecturer)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(length=100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(length=100), index=True, unique=True, nullable=False)
    password = db.Column(db.String(length=256), nullable=False)
    roles = db.Column(db.String(length=100), nullable=False, default="view")

    # Identity function
    def __repr__(self) -> str:
        return '<User {}>'.format(self.username)
    
    # Dictionary function
    def as_dict(self) -> dict:
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # Setting password of user
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Checking if the password of user is correct    
    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)
    
    # Generate auth token
    def generate_auth_token(self, expiration = 60) -> str:
        token = jwt.encode({'id': self.id, 'role': self.roles, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration)}, app.config['SECRET_KEY'], "HS256")
        return token