from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required

from application import db, login_manager
from application.forms import LoginForm, RegisterForm
from application.models import User

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
            remember_me = request.form.getlist('remember_me')
            remember_me = len(remember_me) > 0
            login_user(user, remember=remember_me)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid username/password combination, please try again')
        return redirect(url_for('auth_bp.login'))

    return render_template('login.html', form=form)


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

    return render_template('register.html', form=form)


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
