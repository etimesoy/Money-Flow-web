from datetime import datetime, timedelta

from application.models.currency import Currency
from application.models.transaction import Transaction
from application.models.user_categories_limits_asc import UserCategoriesLimitsAsc


class DatabaseManager:
    @classmethod
    def get_last_7_days_expenses(cls, user_id: int):
        return cls.get_last_7_days_transactions(user_id, expenses=True)

    @classmethod
    def get_last_7_days_incomes(cls, user_id: int):
        return cls.get_last_7_days_transactions(user_id, expenses=False)

    @classmethod
    def get_last_7_days_transactions(cls, user_id: int, expenses: bool = None):
        min_date = datetime.now().date() - timedelta(days=6)
        filters = {
            'user_id': user_id
        }
        if expenses is not None:
            filters['is_expense'] = expenses
        return Transaction.query.filter_by(
            **filters
        ).order_by(
            Transaction.date
        ).where(
            Transaction.date >= min_date
        ).all()

    @classmethod
    def get_all_currencies(cls):
        return Currency.query.all()

    @classmethod
    def get_currency_sign(cls, currency_abbreviation: str):
        return Currency.query.filter_by(
            abbreviation=currency_abbreviation
        ).first().sign
