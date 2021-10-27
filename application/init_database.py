from flask import current_app as app

from application import db
from application.models.category import Category
from application.models.currency import Currency
from application.models.user import User
from application.models.user_categories_limits_asc import UserCategoriesLimitsAsc


def main():
    with app.app_context():
        db.create_all()
        user = User(username='etimesoy', full_name='Руслан Газизов', email='ruslangazizov21@mail.ru')
        user.set_password('123456')
        db.session.add(user)
        for category_id in range(1, 7):
            user_categories_limits_asc = UserCategoriesLimitsAsc(user_id=1, category_id=category_id)
            db.session.add(user_categories_limits_asc)
        db.session.add(Currency(name='Russian Ruble', sign='₽', abbreviation='RUB'))
        db.session.add(Currency(name='US Dollar', sign='$', abbreviation='USD'))
        db.session.add(Currency(name='Euro', sign='€', abbreviation='EUR'))
        db.session.add(Category(name='transport', image='transport.png'))
        db.session.add(Category(name='shopping', image='shopping.png'))
        db.session.add(Category(name='groceries', image='groceries.png'))
        db.session.add(Category(name='health', image='health.png'))
        db.session.add(Category(name='eating out', image='eating_out.png'))
        db.session.add(Category(name='household', image='household.png'))
        db.session.commit()


if __name__ == '__main__':
    main()
