from typing import Dict

from application.services.currency_converter import convert_currency
from application.services.database_manager import DatabaseManager


def get_categories_expenses(user_id: int) -> Dict[str, int]:
    categories_expenses = DatabaseManager.get_total_expenses_in_categories(user_id)
    user_categories_expenses = dict()
    for expense in categories_expenses:
        amount = convert_currency(expense.amount, expense.currency.abbreviation, 'RUB')
        category_name = expense.category.name
        user_categories_expenses[expense.category.name] = user_categories_expenses.get(category_name, 0) + amount
    return user_categories_expenses


def get_categories_limits(user_id: int) -> Dict[str, int]:
    categories_limits = DatabaseManager.get_limits(user_id, in_current_month=True)
    categories_names = map(lambda x: x.category.name, categories_limits)
    categories_limits = map(lambda x: convert_currency(x.limit_size, x.currency.abbreviation, 'RUB'), categories_limits)
    return dict(zip(categories_names, categories_limits))
