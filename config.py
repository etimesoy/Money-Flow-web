class Config:
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    BOOTSTRAP_FONTAWESOME = True
    SECRET_KEY = 'd3s"a5hj;d3]fh4[l'
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


# Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
# RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
# RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'pavel.4.26.21@gmail.com'
    MAIL_PASSWORD = 'rra-cFC-68U-HXh'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    HOSTNAME = 'http://127.0.0.1:5000'


class TestingConfig(Config):
    TESTING = True
