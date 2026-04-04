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
from flask_mail import Mail
from flask_blog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()




def create_app(config_class=Config):
    app = Flask(__name__)
    # Here I create the Flask application instance.
    #  The __name__ parameter helps Flask locate resources like templates and 
    #  static files relative to the current module.

    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    
    from flask_blog.users.routes import users
    app.register_blueprint(users)

    from flask_blog.posts.routes import posts
    app.register_blueprint(posts)

    from flask_blog.main.routes import main
    app.register_blueprint(main)

    from flask_blog.errors.handlers import errors
    app.register_blueprint(errors)

    return app