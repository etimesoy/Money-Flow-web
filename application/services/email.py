from flask import render_template, current_app
from flask_mail import Message

from application import mail
from application.models.user import User


def send_email(user: User):
    app = current_app
    token = user.get_reset_token()

    msg = Message('Request for password restoration - Money Flow',
                  sender=('Ruslan Gazizov from Money Flow', "ruslangazizov36@gmail.com"),
                  recipients=[user.email])
    msg.html = render_template(
        'email/password_reset.html',
        user=user, hostname=app.config['HOSTNAME'], password_reset_code=token
    )
    msg.body = render_template(
        'email/password_reset.txt',
        user=user, hostname=app.config['HOSTNAME'], password_reset_code=token
    )

    with app.app_context():
        mail.send(msg)
