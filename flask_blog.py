from flask import Flask, render_template, url_for
# First I import Flask which is the core framework used to create the web server.
#  I also import render_template which allows me to dynamically render HTML templates, and 
#  url_for which helps generate URLs for routes

app = Flask(__name__)
# Here I create the Flask application instance.
#  The __name__ parameter helps Flask locate resources like templates and 
#  static files relative to the current module.

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
def hello_world():
    return render_template("home.html", posts=posts)
# This function renders the home.html template and passes the posts data into the template. 
# Flask uses the Jinja2 templating engine which allows dynamic rendering of content inside HTML.

@app.route("/about")
def about():
    return render_template("about.html", title='About')


if __name__ == '__main__':
    app.run(debug=True)
    # This condition ensures that the Flask development server runs only when the script is executed directly. 
    # The debug mode allows automatic reload when code changes and provides detailed error messages.