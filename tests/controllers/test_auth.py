from flask import url_for


def test_register_page_content(logged_in_client):
    res = logged_in_client.get(url_for('auth_bp.register'))
    assert res.status_code == 200
    assert b'Register' in res.data
    assert b'Already have an account?' in res.data


def test_register_user_with_invalid_username_should_redirect(logged_in_client):
    res = logged_in_client.post(
        url_for('auth_bp.register'),
        data=dict(full_name='Some name', username=logged_in_client.username, email='test@mail.ru',
                  password='123456', confirm='123456'),
        follow_redirects=True
    )
    assert res.status_code == 200
    assert b'User with such username already exists' in res.data
