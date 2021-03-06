from flask_login import UserMixin

from application import db


class UserCategoriesLimitsAsc(UserMixin, db.Model):
    __tablename__ = 'user_categories_limits_asc'

    __table_args__ = (
        db.PrimaryKeyConstraint("user_id", "category_id"),
        db.CheckConstraint('limit_size IS NULL OR limit_size >= 0')
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    limit_size = db.Column(db.Integer)
    limit_year_number = db.Column(db.Integer)
    limit_month_number = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))

    user = db.relationship('User', backref='user_categories_limits_asc')
    category = db.relationship('Category', backref='user_categories_limits_asc')
    currency = db.relationship('Currency', backref='user_categories_limits_asc')
