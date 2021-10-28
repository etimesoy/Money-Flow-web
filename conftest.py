import pytest
from flask import url_for
from werkzeug.security import generate_password_hash

import wsgi as app_module
from config import TestingConfig
from application import db
from application.models.user import User
from application.models.category import Category
from application.models.currency import Currency
from application.models.user_categories_limits_asc import UserCategoriesLimitsAsc


@pytest.fixture
def app():
    app_module.app.config.from_object(TestingConfig)
    with app_module.app.app_context():
        db.create_all()
    yield app_module.app
    with app_module.app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def logged_in_client(client):
    db.session.add(User(username='etimesoy', full_name='Руслан Газизов', email='ruslangazizov21@mail.ru',
                        password=generate_password_hash('123456', method='sha256')))
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
    client.post(url_for('auth_bp.login'), data=dict(username='etimesoy', password='123456'))
    yield client
    client.get(url_for('auth_bp.logout'))


@pytest.fixture()
def logged_in_another_client(client):
    db.session.add(User(username='test_username', full_name='Test User', email='test_user@mail.ru',
                        password=generate_password_hash('qwerty', method='sha256')))
    db.session.commit()
    client.post(url_for('auth_bp.login'), data=dict(username='test_username', password='qwerty'))
    setattr(client, 'email', 'test_user@mail.ru')
    setattr(client, 'username', 'test_username')
    yield client
    client.get(url_for('auth_bp.logout'))
