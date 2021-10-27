from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from application import db, login_manager
from application.forms import LoginForm, RegisterForm, ForgotPasswordForm, PasswordResetForm
from application.models.user import User
from application.services.email import send_email

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            remember_me = form.remember_me.data
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username/password combination, please try again')
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            user = User(
                username=form.username.data,
                full_name=form.full_name.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        flash('A user with such username already exists')
        return redirect(url_for('auth_bp.register'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
            flash('Email with reset link was sent, please check your inbox')
            return redirect(url_for('auth_bp.forgot_password'))

        flash('Invalid email, please try again')
        return redirect(url_for('auth_bp.forgot_password'))

    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/password_reset/<username>/<password_reset_code>', methods=['GET', 'POST'])
def password_reset(username: str, password_reset_code: str):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = PasswordResetForm()
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('Wrong username - user does not exist')
        return redirect(url_for('auth_bp.forgot_password'))

    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))

    if user.verify_reset_token(password_reset_code, username):
        return render_template('auth/password_reset.html', form=form)
    else:
        flash('Wrong password reset code')
        return redirect(url_for('auth_bp.forgot_password'))


@auth_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
