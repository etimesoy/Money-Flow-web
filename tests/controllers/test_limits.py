import json

import pytest
from flask import url_for

from application.models.user_categories_limits_asc import UserCategoriesLimitsAsc


def test_limits_page_should_redirect_to_login_page_for_not_logged_in_client(client):
    res = client.get(url_for('limits_bp.limits'), follow_redirects=True)
    assert res.status_code == 200
    assert res.request.path == '/login/'


def test_limits_page_should_not_redirect_and_show_limits_for_logged_in_client(logged_in_client):
    res = logged_in_client.get(url_for('limits_bp.limits'), follow_redirects=True)
    assert res.status_code == 200
    assert b'Limits' in res.data


def test_add_limit_page_content(logged_in_client):
    res = logged_in_client.get(url_for('limits_bp.add_limit'))
    assert res.status_code == 200
    assert b'New limit' in res.data
    assert b'Add limit' in res.data


def test_add_limit_action(logged_in_client):
    res = logged_in_client.post(
        url_for('limits_bp.add_limit'),
        data=dict(category='health', size=500, currency='USD', year=2021, month=10),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert res.request.path == '/limits/'
    assert b'health' in res.data
    assert b'500' in res.data
    limit = UserCategoriesLimitsAsc.query.filter_by(
        user_id=logged_in_client.id,
        category_id=4
    ).first()
    assert limit.limit_size == 500
    assert limit.currency_id == 2
    assert limit.limit_month_number == 10
    assert limit.limit_year_number == 2021


def test_limit_info_on_its_page_for_logged_in_client_with_limit(logged_in_client_with_limit):
    res = logged_in_client_with_limit.get(url_for('limits_bp.limits', limit_no=0))
    assert bytes(logged_in_client_with_limit.limit_category, encoding='utf-8') in res.data
    assert bytes(str(logged_in_client_with_limit.limit_size), encoding='utf-8') in res.data


def test_change_limit_info_on_its_page_for_logged_in_client_with_limit(logged_in_client_with_limit):
    res = logged_in_client_with_limit.post(
        url_for('limits_bp.limits', limit_no=0),
        data=dict(category='groceries', size=100, currency='EUR', year=2021, month=10),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert res.request.path == '/limits/'
    assert b'groceries' in res.data
    assert b'100' in res.data


def test_search_limit_by_name_part_for_logged_in_client_with_limit(logged_in_client_with_limit):
    res = logged_in_client_with_limit.post(
        url_for('limits_bp.search_limit_by_name'),
        data=json.dumps(dict(categoryName='hea')),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        mimetype='application/json'
    )
    assert res.status_code == 200
    assert res.content_type == 'application/json'
    assert bytes(logged_in_client_with_limit.limit_category, encoding='utf-8') in res.data
    assert bytes(str(logged_in_client_with_limit.limit_size), encoding='utf-8') in res.data


@pytest.mark.parametrize(['category', 'size', 'currency', 'year', 'month'], [
    ('health', 500, 'USD', 2021, 10),
    ('healthhhhhhh', 500, 'USD', 2021, 10),
    ('health', -500, 'USD', 2021, 10),
    ('health', 500, 'USDDDDDDD', 2021, 10),
    ('health', 500, 'USD', 'twenty twenty-one', 10),
    ('health', 500, 'USD', 2021, 13),
])
def test_add_bad_limits_should_show_warnings(logged_in_client_with_limit, category, size, currency, year, month):
    res = logged_in_client_with_limit.post(
        url_for('limits_bp.add_limit'),
        data=dict(category=category, size=size, currency=currency, year=year, month=month),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b'<script>$("#modal").modal("show")</script>' in res.data
