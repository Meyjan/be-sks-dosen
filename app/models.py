from operator import length_hint
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    username = db.Column(db.String(length=100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(length=100), index=True, unique=True, nullable=False)
    password = db.Column(db.String(length=100), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)