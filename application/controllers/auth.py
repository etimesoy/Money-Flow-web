from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from application import login_manager
from application.forms import LoginForm, RegisterForm, ForgotPasswordForm, PasswordResetForm
from application.services.database_manager import DatabaseManager
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
        user = DatabaseManager.get_user(username=form.username.data)
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
        existing_user = DatabaseManager.get_user(username=form.username.data)
        if existing_user is None:
            new_user = DatabaseManager.add_user(form.username.data, form.password.data, form.full_name.data, form.email.data)
            login_user(new_user)
            DatabaseManager.add_default_categories_to_user(current_user.id)
            return redirect(url_for('index'))

        flash('A user with such username already exists')
        return redirect(url_for('auth_bp.register'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/forgot_password/', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = DatabaseManager.get_user(email=form.email.data)
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
    user = DatabaseManager.get_user(username=username)
    if not user:
        flash('Wrong username - user does not exist')
        return redirect(url_for('auth_bp.forgot_password'))

    if form.validate_on_submit():
        DatabaseManager.update_user_password(username, form.new_password.data)
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
        return DatabaseManager.get_user(user_id=int(user_id))
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))
