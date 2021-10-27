from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from application.services.database_manager import DatabaseManager
from application.services.sidebar_links import get_nav_links

categories_bp = Blueprint(
    'categories_bp', __name__,
    url_prefix='/categories',
    template_folder='templates',
    static_folder='static'
)


@categories_bp.route('/')
@login_required
def categories():
    user_categories = DatabaseManager.get_categories_names(current_user.id)
    return render_template('categories/categories.html',
                           nav_links=get_nav_links(categories=True),
                           enumerated_categories=enumerate(user_categories))


@categories_bp.route('/new/', methods=['GET', 'POST'])
@login_required
def add_category():
    user_categories = DatabaseManager.get_categories_names(current_user.id)
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name in user_categories:
            flash(f'Category {category_name} already exists')
            return redirect(url_for('categories_bp.categories'))

        DatabaseManager.add_category(current_user.id, category_name)
        return redirect(url_for('categories_bp.categories'))

    return render_template('categories/add_category.html',
                           nav_links=get_nav_links(categories=True))
