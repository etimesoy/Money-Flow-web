from flask_login import UserMixin

from application import db


class Currency(UserMixin, db.Model):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    sign = db.Column(db.String(1), nullable=False)
    abbreviation = db.Column(db.String(3), nullable=False, unique=True)
