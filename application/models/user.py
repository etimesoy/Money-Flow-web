from time import time

import jwt
from flask import current_app as app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from application import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    __table_args__ = (
        db.CheckConstraint('len(split(full_name, ' ')) > 1'),
    )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(500), nullable=False)
    full_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)

    def set_password(self, password):
        self.password = generate_password_hash(
            password,
            method='sha256'
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_token(self, expires=500):
        return jwt.encode(
            {'reset_password': self.username, 'exp': time() + expires},
            key=app.secret_key
        ).decode()

    @staticmethod
    def verify_reset_token(token, username):
        try:
            jwt_username = jwt.decode(token, key=app.secret_key)['reset_password']
        except Exception as e:
            print(e)
            return False
        else:
            return jwt_username == username

    def __repr__(self):
        return f'<User {self.username}>'
