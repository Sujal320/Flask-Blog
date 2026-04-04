import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # The application is configured using Flask’s configuration system. 
    # I defined a SECRET_KEY which is required by Flask-WTF to securely handle form submissions and CSRF protection.

    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')