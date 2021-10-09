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


class TestingConfig(Config):
    TESTING = True
