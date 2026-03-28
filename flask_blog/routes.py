from flask import render_template, url_for, flash, redirect
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm


from flask_blog.models import User, Post

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
    # The validate_on_submit() method checks two things: 
    # first, whether the request method is POST
    # second, whether all the form validators pass successfully
    if form.validate_on_submit():
        # if the form is validated before we make instance of the user in our database we hash the user's password
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # creating the user instance in user database
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        # adding user to database and commiting
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        # Flash messages are used to send temporary feedback to the user after an action occurs
        return redirect(url_for('login'))
        # After successful form submission, the user is redirected to the login page using redirect and url_for
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