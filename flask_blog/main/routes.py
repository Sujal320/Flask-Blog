from flask import render_template, request
from flask_blog.models import Post
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route("/") #Flask uses decorators to define routes. 
@main.route("/home") #These routes map specific URLs to Python functions.
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template("home.html", posts=posts)
# This function renders the home.html template and passes the posts data into the template. 
# Flask uses the Jinja2 templating engine which allows dynamic rendering of content inside HTML.

@main.route("/about")
def about():
    return render_template("about.html", title='About')


