from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from app.configuration import DevelopmentConfig

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    from . import models

    app = Flask(__name__, static_folder='templates', instance_relative_config=False)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        from . import routes
        from . import auth

        app.register_blueprint(auth.auth_bp)

        db.create_all()

        return app
