from datetime import date, datetime
from calendar import TextCalendar
import calendar

import pytest
from flask import url_for


def test_main_page_should_redirect_to_login_page_for_not_logged_in_client(client):
    res = client.get(url_for('index'), follow_redirects=True)
    assert res.status_code == 200
    assert b'<title>Money Flow - Login</title>' in res.data


def test_main_page_should_not_redirect_and_show_overview_for_logged_in_client(logged_in_client):
    res = logged_in_client.get(url_for('index'))
    assert res.status_code == 200
    assert b'Overview' in res.data
    assert b'Transactions' in res.data


def test_add_transaction_page_should_not_redirect_and_show_add_transaction_form(logged_in_client):
    res = logged_in_client.get(url_for('add_transaction'))
    assert res.status_code == 200
    assert b'New transaction' in res.data
    assert b'Add transaction' in res.data


@pytest.mark.parametrize(['tr_type', 'tr_date', 'name', 'amount', 'currency', 'category'], [
    ('expense', date(2021, 10, 28), 'New expense', 100, 'USD', 'health'),
    ('income', date(2021, 10, 28), 'New income', 100, 'RUB', ''),
])
def test_add_transactions_for_logged_in_client_should_be_ok(logged_in_client, tr_type, tr_date,
                                                            name, amount, currency, category):
    res = logged_in_client.post(
        url_for('add_transaction'),
        data=dict(type=tr_type, date=tr_date, name=name, amount=amount, currency=currency, category=category),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert res.request.path == '/'
    assert b'<td>' + bytes(name, encoding='utf-8') + b'</td>' in res.data


@pytest.mark.parametrize(['tr_type', 'tr_date', 'name', 'amount', 'currency', 'category'], [
    ('some_wrong_transaction_type', date(2021, 10, 28), 'some name', 100, 'RUB', 'health'),
    ('expense', '28.10.2021', 'some name', 100, 'RUB', 'health'),
    ('expense', date(2021, 10, 28), '', 100, 'RUB', 'health'),
    ('expense', date(2021, 10, 28), 'some name', -100, 'RUB', 'health'),
    ('expense', date(2021, 10, 28), 'some name', 100, 'RUBBBBBBB', 'health'),
    ('expense', date(2021, 10, 28), 'some name', 100, 'RUB', 'healthhhhhhh'),
    ('income', date(2021, 10, 28), 'some name', 100, 'RUB', 'health'),
])
def test_add_bad_transactions_should_show_warnings(logged_in_client, tr_type, tr_date,
                                                   name, amount, currency, category):
    res = logged_in_client.post(
        url_for('add_transaction'),
        data=dict(type=tr_type, date=tr_date, name=name, amount=amount, currency=currency, category=category),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b'<script>$("#modal").modal("show")</script>' in res.data


def test_month_time_interval_display_on_main_page(logged_in_client):
    current_year, current_month = datetime.now().year, datetime.now().month
    current_month_name = TextCalendar().formatmonthname(current_year, current_month, 0, withyear=False)
    _, current_month_days_count = calendar.monthrange(year=current_year, month=current_month)
    res = logged_in_client.get(url_for('index', time_interval='month'))
    assert res.status_code == 200
    for i in range(1, current_month_days_count + 1):
        assert bytes(str(i) + ' ' + current_month_name, encoding='utf-8') in res.data
