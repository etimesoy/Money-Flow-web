from flask_wtf import FlaskForm
from wtforms import DateTimeField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


# recaptcha = RecaptchaField('Recaptcha')

class LoginForm(FlaskForm):
    username = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[
        Length(min=6),
        Email(message='Enter a valid email.'),
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Select a stronger password.')
    ])
    confirm = PasswordField('Confirm Your Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Register')
