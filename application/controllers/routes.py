from datetime import date

from flask import render_template, redirect, url_for, request, flash
from flask import current_app as app
from flask_login import current_user, login_required

from application.services.currency_converter import convert_currency
from application.services.database_manager import DatabaseManager
from application.services.date_handlers import get_month_days_count, get_offset_year_month, get_month_days
from application.services.offsets import get_offset_week_days, offset_list
from application.services.sidebar_links import get_nav_links


@app.route('/')
def index():
    if current_user.is_authenticated:
        currency_abbreviation = request.args.get('currency', 'RUB')
        time_interval = request.args.get('time_interval', 'week')
        time_interval_offset = request.args.get('offset', '0')
        try:
            time_interval_offset = int(time_interval_offset)
        except ValueError:
            time_interval_offset = 0
        show = request.args.get('show', 'all')
        if show == 'expenses':
            expenses = True
        elif show == 'incomes':
            expenses = False
        else:
            expenses = None

        if time_interval == 'week':
            last_transactions = DatabaseManager.get_days_transactions(current_user.id, time_interval_offset, expenses=expenses)
            total_expenses_for_time_interval, total_incomes_for_time_interval = [0] * 7, [0] * 7
        else:  # time_interval == 'month'
            month_days_count = get_month_days_count(time_interval_offset)
            offset_year, offset_month = get_offset_year_month(time_interval_offset)
            last_transactions = DatabaseManager.get_month_transactions(current_user.id, offset_year, offset_month, expenses=expenses)
            total_expenses_for_time_interval, total_incomes_for_time_interval = [0] * month_days_count, [0] * month_days_count

        show_week = time_interval == 'week'
        for transaction in last_transactions:
            amount = convert_currency(transaction.amount, transaction.currency.abbreviation, currency_abbreviation)
            transaction_weekday = transaction.date.weekday()
            transaction_day = transaction.date.day - 1
            if transaction.is_expense:
                total_expenses_for_time_interval[transaction_weekday if show_week else transaction_day] += amount
            else:
                total_incomes_for_time_interval[transaction_weekday if show_week else transaction_day] += amount

        if show_week:
            days_labels, offset_value = get_offset_week_days(return_offset=True)
            total_expenses_for_time_interval = offset_list(total_expenses_for_time_interval, offset_value)
            total_incomes_for_time_interval = offset_list(total_incomes_for_time_interval, offset_value)
        else:
            days_labels = get_month_days(time_interval_offset)
        currency_sign = DatabaseManager.get_currency_sign(currency_abbreviation)
        currencies = DatabaseManager.get_all_currencies()
        total_transactions = DatabaseManager.get_transactions(current_user.id, expenses=expenses)
        return render_template('transactions/transactions.html', total_transactions=total_transactions,
                               last_expenses=total_expenses_for_time_interval,
                               last_incomes=total_incomes_for_time_interval,
                               labels=days_labels, currency_sign=currency_sign,
                               currencies=currencies, nav_links=get_nav_links(overview=True))

    return redirect(url_for('auth_bp.login'))


@app.route('/transactions/new/', methods=['GET', 'POST'])
@login_required
def add_transaction():
    if request.method == 'POST':
        transaction_type = request.form.get('type')
        transaction_date = request.form.get('date')
        name = request.form.get('name')
        amount = request.form.get('amount')
        currency_abbreviation = request.form.get('currency')
        category = request.form.get('category')

        if not check_transaction_info(transaction_type, transaction_date,
                                      name, amount, currency_abbreviation, category):
            return redirect(url_for('add_transaction'))

        DatabaseManager.add_transaction(current_user.id, transaction_type.lower() == 'expense',
                                        date.fromisoformat(transaction_date),
                                        amount, category, name, currency_abbreviation)
        return redirect(url_for('index'))

    return render_template('transactions/add_transaction.html',
                           nav_links=get_nav_links(overview=True))


def check_transaction_info(transaction_type: str, transaction_date: str,
                           name: str, amount: str, currency_abbreviation: str,
                           category: str) -> bool:
    categories_names = DatabaseManager.get_categories_names(current_user.id)
    currencies = DatabaseManager.get_all_currencies()
    currencies_abbreviations = list(map(lambda x: x.abbreviation, currencies))

    if transaction_type.lower() not in ['expense', 'income']:
        flash('Transaction type should be expense or income')
        return False
    try:
        date.fromisoformat(transaction_date)
    except TypeError:
        flash('Date should be date-like')
        return False
    if len(name) == 0:
        flash('Name should be present')
        return False
    if not amount.isdigit() or int(amount) <= 0:
        flash('Amount should be a positive integer')
        return False
    if currency_abbreviation not in currencies_abbreviations:
        flash(f'Currency abbreviation should be one of the following: {currencies_abbreviations}')
        return False
    if transaction_type.lower() == 'expense' and category.lower() not in categories_names:
        flash(f'Category name should be one of the following: {categories_names}')
        return False
    return True
