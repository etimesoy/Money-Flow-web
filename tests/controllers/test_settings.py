import pytest
from flask import url_for
from flask_login import current_user


def test_current_user_info_for_logged_out_should_not_be_ok(client):
    res = client.get(url_for('settings_bp.settings'), follow_redirects=True)
    assert res.status_code == 200
    assert b'You must be logged in to view that page' in res.data
    assert b'etimesoy' not in res.data


def test_current_user_info_for_logged_in_should_be_ok(logged_in_client):
    res = logged_in_client.get(url_for('settings_bp.settings'))
    assert res.status_code == 200
    assert b'You must be logged in to view that page' not in res.data
    assert b'etimesoy' in res.data
    assert bytes('Руслан Газизов', encoding='utf-8') in res.data
    assert b'ruslangazizov21@mail.ru' in res.data


@pytest.mark.parametrize(['username', 'full_name'], [
    ('etimesoy2', 'Руслан2 Газизов2'),
    ('etimesoy', 'Руслан Газизов')
])
def test_change_current_user_info_for_logged_in_should_be_ok(logged_in_client, username, full_name):
    res = logged_in_client.post(url_for('settings_bp.settings'),
                                data=dict(username=username, full_name=full_name, email=current_user.email),
                                follow_redirects=True)
    assert res.status_code == 200
    assert b'Your settings have been successfully changed' in res.data
    assert bytes(username, encoding='utf-8') in res.data
    assert bytes(full_name, encoding='utf-8') in res.data
    assert b'ruslangazizov21@mail.ru' in res.data


def test_change_current_user_email_to_another_user_email_should_not_be_ok(logged_in_client, logged_in_another_client):
    another_user_email = logged_in_another_client.email
    res = logged_in_client.post(
        url_for('settings_bp.settings'),
        data=dict(username=current_user.username, full_name=current_user.full_name, email=another_user_email),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b'User with such email already exists' in res.data


def test_change_current_user_username_to_another_user_username_should_not_be_ok(logged_in_client,
                                                                                logged_in_another_client):
    another_user_username = logged_in_another_client.username
    res = logged_in_client.post(
        url_for('settings_bp.settings'),
        data=dict(username=another_user_username, full_name=current_user.full_name, email=current_user.email),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b'User with such username already exists' in res.data


def test_change_current_user_full_name_to_invalid_full_name_should_not_be_ok(logged_in_client):
    res = logged_in_client.post(
        url_for('settings_bp.settings'),
        data=dict(username=current_user.username, full_name='SingleWordWithoutSpaces', email=current_user.email),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b'Full name must contain at least two words' in res.data
