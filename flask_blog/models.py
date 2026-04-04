from datetime import datetime, timezone
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_blog import db, login_manager, app
from flask_login import UserMixin
# UserMixin provides default implementations of methods required by Flask-Login
# Without UserMixin, your User class must define: is_authenticated, is_active, get_id()...

# This function tells Flask-Login how to reload a user from the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# The User model represents a table in the database. Each instance of the class corresponds to a row in the table
class User(db.Model, UserMixin):
    # Each column defines constraints such as uniqueness and nullability, ensuring data integrity
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True) #The backref creates a reverse reference so each post can access its author directly
    # defined a one-to-many relationship between User and Post, where a user can have multiple posts. 
    # This is implemented using SQLAlchemy’s relationship function.

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


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