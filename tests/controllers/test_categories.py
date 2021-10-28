from flask import url_for


def test_categories_page_should_not_redirect_and_show_categories(logged_in_client):
    res = logged_in_client.get(url_for('categories_bp.categories'))
    assert res.status_code == 200
    assert b'Categories' in res.data
    assert b'This month total expenses' in res.data
    assert b'health' in res.data


def test_add_category_page_content(logged_in_client):
    res = logged_in_client.get(url_for('categories_bp.add_category'))
    assert res.status_code == 200
    assert b'New category' in res.data
    assert b'Add category' in res.data
