# FlaskForm is the base class used to define forms in Flask applications
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')