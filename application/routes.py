from flask import render_template, redirect, url_for, request
from flask import current_app as app
from flask_login import current_user, login_required

from application.services.currency_converter import convert_currency
from application.services.database_manager import DatabaseManager
from application.services.get_offset_week_days import get_offset_week_days


@app.route('/')
def index():
    if current_user.is_authenticated:
        currency_abbreviation = request.args.get('currency', 'RUB')
        transactions = list(DatabaseManager.get_last_7_days_transactions(current_user.id))
        last_7_days_total_expenses, last_7_days_total_incomes = [0] * 7, [0] * 7
        for transaction in transactions:
            amount = convert_currency(transaction.amount, transaction.currency.abbreviation, currency_abbreviation)
            transaction_weekday = transaction.date.weekday()
            if transaction.is_expense:
                last_7_days_total_expenses[transaction_weekday] += amount
            else:
                last_7_days_total_incomes[transaction_weekday] += amount
        offset_week_days = get_offset_week_days()
        currency_sign = DatabaseManager.get_currency_sign(currency_abbreviation)
        currencies = DatabaseManager.get_all_currencies()
        return render_template('main.html', labels=offset_week_days, currency_sign=currency_sign,
                               expenses=last_7_days_total_expenses, incomes=last_7_days_total_incomes,
                               transactions=transactions, currencies=currencies)

    return redirect(url_for('auth_bp.login'))


@app.route('/currency/<currency_abbreviation>/')
@login_required
def change_currency(currency_abbreviation: str):
    return redirect(url_for('index', currency=currency_abbreviation))
