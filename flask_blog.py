
from datetime import datetime, timezone
from flask import Flask, render_template, url_for, flash, redirect
# First I import Flask which is the core framework used to create the web server.
#  I also import render_template which allows me to dynamically render HTML templates, and 
#  url_for which helps generate URLs for routes
from forms import RegistrationForm, LoginForm

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Here I create the Flask application instance.
#  The __name__ parameter helps Flask locate resources like templates and 
#  static files relative to the current module.

app.config['SECRET_KEY'] = 'c3136bac1cbbf1f5b906d44fd17c6c84'
# The application is configured using Flask’s configuration system. 
# I defined a SECRET_KEY which is required by Flask-WTF to securely handle form submissions and CSRF protection.

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

posts = [
    {
        'author': 'ketchupOnCereals',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'June 22 2004'
    },
    {
        'author': 'koc',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'June 22 2005'
    }
]
# For now I am using a simple in-memory data structure to simulate a database

@app.route("/") #Flask uses decorators to define routes. 
@app.route("/home") #These routes map specific URLs to Python functions.
def home():
    return render_template("home.html", posts=posts)
# This function renders the home.html template and passes the posts data into the template. 
# Flask uses the Jinja2 templating engine which allows dynamic rendering of content inside HTML.

@app.route("/about")
def about():
    return render_template("about.html", title='About')

# This route handles the user registration page. 
# It accepts both GET and POST requests. 
# A GET request loads the registration form, while a POST request processes the submitted form data
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # The validate_on_submit() method checks two things: 
        # first, whether the request method is POST
        # second, whether all the form validators pass successfully
        flash(f'Account created for {form.username.data}!', 'success')
        # Flash messages are used to send temporary feedback to the user after an action occurs
        return redirect(url_for('home'))
        # After successful form submission, the user is redirected to the home page using redirect and url_for
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # This condition ensures that the Flask development server runs only when the script is executed directly. 
    # The debug mode allows automatic reload when code changes and provides detailed error messages.