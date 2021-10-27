from flask import Flask
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import DevelopmentConfig

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app():
    from . import models

    app = Flask(__name__, static_folder='static', template_folder='templates', instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)

    app.jinja_env.add_extension('jinja2.ext.do')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from application.controllers import routes, auth, settings, limits, categories

        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(settings.settings_bp)
        app.register_blueprint(limits.limits_bp)
        app.register_blueprint(categories.categories_bp)

        return app
