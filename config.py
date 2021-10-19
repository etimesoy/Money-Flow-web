from environs import Env

env = Env()
env.read_env()


class Config:
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    TESTING = False
    BOOTSTRAP_FONTAWESOME = True
    CSRF_ENABLED = True
    SECRET_KEY = env.str('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_LOCAL_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


# Get your reCaptche key on: https://www.google.com/recaptcha/admin/create
# RECAPTCHA_PUBLIC_KEY = "6LffFNwSAAAAAFcWVy__EnOCsNZcG2fVHFjTBvRP"
# RECAPTCHA_PRIVATE_KEY = "6LffFNwSAAAAAO7UURCGI7qQ811SOSZlgU69rvv7"

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = env.str('SQLALCHEMY_PRODUCTION_DATABASE_URI')
    HOSTNAME = env.str('PRODUCTION_HOSTNAME')


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = env.str('GMAIL_USERNAME')
    MAIL_PASSWORD = env.str('GMAIL_PASSWORD')
    HOSTNAME = env.str('DEVELOPMENT_HOSTNAME')


class TestingConfig(Config):
    TESTING = True
