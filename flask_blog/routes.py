import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_blog import app, db, bcrypt
from flask_blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog.models import User, Post



@app.route("/") #Flask uses decorators to define routes. 
@app.route("/home") #These routes map specific URLs to Python functions.
def home():
    posts = Post.query.all()
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # looking for the user in our database
        user = User.query.filter_by(email=form.email.data).first()
        # verifying the ceredentials and user flask_login extension to handle login
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # this next_page is like holding till you login and then only let you immediately access
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Profile_Pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='Profile_Pics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required # login requrired decorator
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', category='success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)