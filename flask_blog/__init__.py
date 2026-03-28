from datetime import datetime, timezone
from flask import Flask
# First I import Flask which is the core framework used to create the web server.
#  I also import render_template which allows me to dynamically render HTML templates, and 
#  url_for which helps generate URLs for routes
from flask_bcrypt import Bcrypt
# using bcrypt (a python library) to hash our passwords in our database
from flask_login import LoginManager
# Flask-Login that manages user session handling, 
# such as logging users in, remembering them, and 
# loading user data from the database
from flask_sqlalchemy import SQLAlchemy
# integrated a database into my Flask application using SQLAlchemy ORM,
# which allows me to define database tables as Python classes and 
# interact with them using objects instead of raw SQL queries


app = Flask(__name__)
# Here I create the Flask application instance.
#  The __name__ parameter helps Flask locate resources like templates and 
#  static files relative to the current module.

app.config['SECRET_KEY'] = 'c3136bac1cbbf1f5b906d44fd17c6c84'
# The application is configured using Flask’s configuration system. 
# I defined a SECRET_KEY which is required by Flask-WTF to securely handle form submissions and CSRF protection.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from flask_blog import routes