from flask import render_template, redirect, url_for
from flask import current_app as app
from flask_login import current_user


@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main.html')
    return redirect(url_for('auth_bp.login'))
