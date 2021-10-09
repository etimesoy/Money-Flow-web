from flask import Blueprint, render_template
from flask_login import login_required

settings_bp = Blueprint(
    'settings_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@settings_bp.route('/settings/')
@login_required
def settings():
    return render_template('settings.html')
