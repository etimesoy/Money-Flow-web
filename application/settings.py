from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user

from application.services.database_manager import DatabaseManager
from application.services.sidebar_links import get_nav_links

settings_bp = Blueprint(
    'settings_bp', __name__,
    url_prefix='/settings',
    template_folder='templates',
    static_folder='static'
)


@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        username = request.form.get('username')
        full_name = request.form.get('full_name')
        email = request.form.get('email')

        if not check_user_info(username, full_name, email):
            return redirect(url_for('settings_bp.settings'))

        DatabaseManager.update_user(current_user.id, username, full_name, email)
        flash('Your settings have been successfully changed')
        return redirect(url_for('settings_bp.settings'))

    return render_template('settings/settings.html',
                           nav_links=get_nav_links(settings=True),
                           user_info=current_user)


def check_user_info(username: str, full_name: str, email: str):
    if len(full_name.split(' ')) < 2:
        flash('Full name must contain at least two words')
        return False
    if username != current_user.username:
        user = DatabaseManager.get_user(username=username)
        if user is not None:
            flash('User with such username already exists')
            return False
    if email != current_user.email:
        user = DatabaseManager.get_user(email=email)
        if user is not None:
            flash('User with such email already exists')
            return False
    return True
