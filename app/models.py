from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return '<User {}>'.format(self.username)