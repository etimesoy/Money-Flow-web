from datetime import datetime, timedelta, date
from typing import List

from sqlalchemy import text, String

from application import db
from application.models.category import Category
from application.models.currency import Currency
from application.models.transaction import Transaction
from application.models.user import User
from application.models.user_categories_limits_asc import UserCategoriesLimitsAsc


class LimitAlreadyExistsError(Exception):
    pass


class DatabaseManager:
    @classmethod
    def get_all_currencies(cls):
        return list(Currency.query.all())

    @classmethod
    def get_currency_sign(cls, currency_abbreviation: str):
        with db.engine.connect() as conn:
            query = text("""
            SELECT sign FROM currencies
            WHERE abbreviation=:currency_abbreviation
            """)
            result = conn.execute(query, currency_abbreviation=currency_abbreviation).fetchone()
        return result[0]

    @classmethod
    def get_currency_id(cls, currency_abbreviation: str):
        return Currency.query.filter_by(
            abbreviation=currency_abbreviation
        ).first().id

    @classmethod
    def get_category_id(cls, name: str):
        return Category.query.filter_by(
            name=name
        ).first().id

    @classmethod
    def get_user(cls, user_id: int = None,
                 username: str = None,
                 password: str = None,
                 full_name: str = None,
                 email: str = None) -> User:
        filters = dict(id=user_id, username=username, password=password, full_name=full_name, email=email)
        filters = {key: value for key, value in filters.items() if value is not None}
        return User.query.filter_by(
            **filters
        ).first()

    @classmethod
    def get_transactions(cls, user_id: int, expenses: bool = None) -> List[Transaction]:
        filters = {
            'user_id': user_id
        }
        if expenses is not None:
            filters['is_expense'] = expenses
        return list(Transaction.query.filter_by(
            **filters
        ).all())

    @classmethod
    def get_days_transactions(cls, user_id: int, offset_weeks_count: int = 0, expenses: bool = None) -> List[Transaction]:
        max_date = datetime.now().date() + timedelta(days=offset_weeks_count * 7)
        min_date = max_date - timedelta(days=6)
        filters = {
            'user_id': user_id
        }
        if expenses is not None:
            filters['is_expense'] = expenses
        return list(Transaction.query.filter_by(
            **filters
        ).order_by(
            Transaction.date
        ).where(
            Transaction.date >= min_date,
            Transaction.date <= max_date
        ).all())

    @classmethod
    def get_month_transactions(cls, user_id: int,
                               year_no: int,
                               month_no: int,
                               expenses: bool = None) -> List[Transaction]:
        filters = {
            'user_id': user_id,
        }
        if expenses is not None:
            filters['is_expense'] = expenses
        if month_no <= 9:
            month_no = '0' + str(month_no)
        return list(Transaction.query.filter_by(
            **filters
        ).order_by(
            Transaction.date
        ).where(
            Transaction.date.cast(String).like(f'{year_no}-{month_no}-%')
        ).all())

    @classmethod
    def get_limits(cls, user_id: int, in_current_month: bool = False) -> List[UserCategoriesLimitsAsc]:
        filters = {}
        if in_current_month:
            filters['limit_month_number'] = datetime.now().month
            filters['limit_year_number'] = datetime.now().year
        return list(UserCategoriesLimitsAsc.query.filter_by(
            user_id=user_id, **filters
        ).where(
            UserCategoriesLimitsAsc.limit_size.is_not(None)
        ).order_by(
            UserCategoriesLimitsAsc.category_id
        ).all())

    @classmethod
    def get_limits_by_category_name_part(cls,
                                         user_id: int,
                                         category_name: str) -> list:
        return UserCategoriesLimitsAsc.query.join(
            Category
        ).filter(
            UserCategoriesLimitsAsc.user_id == user_id,
            Category.name.ilike(f'%{category_name}%')
        ).where(
            UserCategoriesLimitsAsc.limit_size.is_not(None)
        ).order_by(
            UserCategoriesLimitsAsc.category_id
        ).all()

    @classmethod
    def get_categories_names(cls, user_id: int) -> List[str]:
        user_categories_limits = list(UserCategoriesLimitsAsc.query.filter_by(
            user_id=user_id
        ).all())
        return list(map(lambda x: x.category.name, user_categories_limits))

    @classmethod
    def get_total_expenses_in_categories(cls, user_id: int):
        user_categories_expenses = list(Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.is_expense
        ).all())
        return user_categories_expenses

    @classmethod
    def update_user(cls, user_id: int, username: str, full_name: str, email: str):
        user = User.query.filter_by(
            id=user_id
        ).first()
        user.username = username
        user.full_name = full_name
        user.email = email
        db.session.commit()

    @classmethod
    def add_user(cls, username: str, password: str, full_name: str, email: str) -> User:
        user = User(
            username=username,
            full_name=full_name,
            email=email
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def add_default_categories_to_user(cls, user_id: int):
        for category_id in range(1, 7):
            user_categories_limits_asc = UserCategoriesLimitsAsc(
                user_id=user_id, category_id=category_id
            )
            db.session.add(user_categories_limits_asc)
        db.session.commit()

    @classmethod
    def add_transaction(cls, user_id: int,
                        is_expense: bool,
                        transaction_date: date,
                        amount: int,
                        category_name: str,
                        transaction_name: str,
                        currency_abbreviation: str):
        currency_id = cls.get_currency_id(currency_abbreviation)
        new_transaction = Transaction(
            user_id=user_id,
            is_expense=is_expense,
            date=transaction_date,
            amount=amount,
            name=transaction_name,
            currency_id=currency_id
        )
        if len(category_name) > 0:
            category_id = cls.get_category_id(category_name)
            new_transaction.category_id = category_id
        db.session.add(new_transaction)
        db.session.commit()

    @classmethod
    def add_category(cls, user_id: int, category_name: str):
        new_category = Category(
            name=category_name,
            image=category_name + '.png'
        )
        db.session.add(new_category)
        db.session.commit()
        category_id = cls.get_category_id(category_name)
        new_user_category_limit_asc = UserCategoriesLimitsAsc(
            user_id=user_id,
            category_id=category_id
        )
        db.session.add(new_user_category_limit_asc)
        db.session.commit()

    @classmethod
    def add_limit(cls, user_id: int,
                  category_name: str,
                  size: int,
                  currency_abbreviation: str,
                  year: int,
                  month_number: int):
        category_id = cls.get_category_id(category_name)
        user_category_limit_asc = UserCategoriesLimitsAsc.query.filter_by(
            user_id=user_id,
            category_id=category_id
        ).first()
        if user_category_limit_asc.limit_size is not None:
            raise LimitAlreadyExistsError(f'Limit for category {category_name} already exists')

        currency_id = cls.get_currency_id(currency_abbreviation)
        user_category_limit_asc.limit_size = size
        user_category_limit_asc.limit_year_number = year,
        user_category_limit_asc.limit_month_number = month_number,
        user_category_limit_asc.currency_id = currency_id
        db.session.commit()

    @classmethod
    def update_limit(cls, user_id: int,
                     category_name: str,
                     size: int,
                     currency_abbreviation: str,
                     year: int,
                     month_number: int):
        category_id = cls.get_category_id(category_name)
        currency_id = cls.get_currency_id(currency_abbreviation)
        user_categories_limits_asc = UserCategoriesLimitsAsc.query.filter_by(
            user_id=user_id,
            category_id=category_id
        ).first()
        user_categories_limits_asc.limit_size = size
        user_categories_limits_asc.limit_month_number = month_number
        user_categories_limits_asc.limit_year_number = year
        user_categories_limits_asc.currency_id = currency_id
        db.session.commit()

    @classmethod
    def update_user_password(cls, username: str, new_password: str):
        user = User.query.filter_by(username=username).first()
        user.set_password(new_password)
        db.session.commit()
