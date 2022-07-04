from sqlalchemy import ForeignKey
from app import app, db
from app.models.user import User

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    sks1_score = db.Column(db.Integer, nullable=False)
    sks2_score = db.Column(db.Integer, nullable=False)
    sks3_score = db.Column(db.Integer, nullable=False)
    support_score = db.Column(db.Integer, nullable=False)
    cluster = db.Column(db.Integer)

    uc_args_1 = db.UniqueConstraint(user_id, year)
    __tableargs__ = (uc_args_1)

    # Identity function
    def __repr__(self):
        return '<Score {} at year {}>'.format(self.user_id, self.year)