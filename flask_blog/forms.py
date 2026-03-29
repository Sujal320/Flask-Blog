# FlaskForm is the base class used to define forms in Flask applications
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_blog.models import User

# FlaskForm is the base class provided by Flask-WTF that adds 
# form handling functionality such as validation, CSRF protection, and integration with Flask templates
class RegistrationForm(FlaskForm):
    # In Flask-WTF, forms are defined as Python classes. 
    # Each class represents a form and contains fields along with their validation rules.
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    # “Each form field is defined using WTForms fields and validators. 
    # For example, the username field ensures the input is required and limits the length between 2 and 20 characters
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # for account already exist in the database 
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')  
        

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', 
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose a different one.')  
        

class PostForm(FlaskForm):
    title = StringField('Title',
                        validators=[DataRequired()])
    content = TextAreaField('Content',
                            validators=[DataRequired()])
    submit = SubmitField('Post')