from flask_login import UserMixin

from application import db


class Category(UserMixin, db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    image = db.Column(db.String(100), nullable=False)
