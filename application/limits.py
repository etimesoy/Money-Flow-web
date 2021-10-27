from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from application.services.database_manager import DatabaseManager, LimitAlreadyExistsError
from application.services.sidebar_links import get_nav_links

limits_bp = Blueprint(
    'limits_bp', __name__,
    url_prefix='/limits',
    template_folder='templates',
    static_folder='static'
)


@limits_bp.route('/')
@limits_bp.route('/<int:limit_no>/', methods=['GET', 'POST'])
@login_required
def limits(limit_no: int = None):
    user_limits = DatabaseManager.get_limits(current_user.id)
    if limit_no is None:
        return render_template('limits/limits.html',
                               nav_links=get_nav_links(limits=True),
                               enumerated_limits=enumerate(user_limits))

    if request.method == 'POST':
        category = request.form.get('category')
        size = request.form.get('size')
        currency_abbreviation = request.form.get('currency')
        year = request.form.get('year')
        month_number = request.form.get('month')

        if not check_limit_info(category, size, currency_abbreviation, year, month_number):
            return redirect(url_for('limits_bp.limits', limit_no=limit_no))

        DatabaseManager.update_limit(current_user.id, category, int(size),
                                     currency_abbreviation, int(year), int(month_number))
        return redirect(url_for('limits_bp.limits'))

    return render_template('limits/limit.html',
                           nav_links=get_nav_links(limits=True),
                           limit_info=user_limits[limit_no])


@limits_bp.route('/new/', methods=['GET', 'POST'])
@login_required
def add_limit():
    if request.method == 'POST':
        category = request.form.get('category')
        size = request.form.get('size')
        currency_abbreviation = request.form.get('currency')
        year = request.form.get('year')
        month_number = request.form.get('month')

        if not check_limit_info(category, size, currency_abbreviation, year, month_number):
            return redirect(url_for('limits_bp.add_limit'))

        try:
            DatabaseManager.add_limit(current_user.id, category, size, currency_abbreviation, year, month_number)
        except LimitAlreadyExistsError as e:
            flash(str(e) or 'Unknown error')
        finally:
            return redirect(url_for('limits_bp.limits'))

    return render_template('limits/add_limit.html',
                           nav_links=get_nav_links(limits=True))


@limits_bp.route('/search/', methods=['GET', 'POST'])
@login_required
def search_department_by_name():
    json_content = request.get_json()
    user_limits = DatabaseManager.get_limits_by_category_name_part(current_user.id, json_content['categoryName'])
    result = []
    """
    <td><a href="{{ url_for("limits_bp.limits", limit_no=idx) }}">{{ idx }}</a></td>
    <td>{{ limit.category.name }}</td>
    <td>{{ limit.limit_size }}</td>
    <td>{{ limit.currency.abbreviation }}</td>
    <td>{{ limit.limit_year_number }}</td>
    <td>{{ limit.limit_month_number }}</td>
    """
    for idx, limit in enumerate(user_limits):
        result.append([
            f'<a href="{ url_for("limits_bp.limits", limit_no=idx) }">{ idx }</a>',
            limit.category.name,
            limit.limit_size,
            limit.currency.abbreviation,
            limit.limit_year_number,
            limit.limit_month_number
        ])
    return jsonify(result)


def check_limit_info(category: str, size: str, currency_abbreviation: str, year: str, month_number: str) -> bool:
    categories_names = DatabaseManager.get_categories_names(current_user.id)
    currencies = DatabaseManager.get_all_currencies()
    currencies_abbreviations = list(map(lambda x: x.abbreviation, currencies))

    if category.lower() not in categories_names:
        flash(f'Category name should be one of the following: {categories_names}')
        return False
    if not size.isdigit() or int(size) <= 0:
        flash('Size should be a non-negative integer')
        return False
    if currency_abbreviation not in currencies_abbreviations:
        flash(f'Currency abbreviation should be one of the following: {currencies_abbreviations}')
        return False
    if not year.isdigit() or int(year) <= 0:
        flash('Year should be a positive integer')
        return False
    if not month_number.isdigit() or int(month_number) <= 0 or int(month_number) >= 13:
        flash('Month should be an integer between 1 and 12')
        return False
    return True
