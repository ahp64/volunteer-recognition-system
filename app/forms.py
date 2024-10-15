# Flask modules
from flask_wtf import FlaskForm
from wtforms.validators import ValidationError
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

# Local modules
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'placeholder': 'example@email.com'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': '********'})
    remember_me = BooleanField('Remember me', default=False)
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Name must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(),
        Email("Must be a valid email address.")
    ], render_kw={'placeholder': 'example@email.com'})
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8),
    ], render_kw={'placeholder': 'Enter your password'})
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ],
                                     render_kw={'placeholder': 'Confirm your password'})
    submit = SubmitField('Register')

    # Prevents duplicate accounts
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).one_or_none()
        if existing_user:
            raise ValidationError('Email address already registered.')

    def validate_password(self, password):
        # Consider adding special character requirements
        if not any(c.isalpha() for c in password.data) or not any(c.isdigit() for c in password.data):
            raise ValidationError('Password must contain at least one letter and one digit.')

class ProfileForm(FlaskForm):
    # https://wtforms.readthedocs.io/en/3.1.x/validators/#built-in-validators
    # TODO: Work with validators to see how to work with required / non-required input
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=80),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Name must contain only letters, numbers, and underscores.')],
                       render_kw={'placeholder': 'Display name'})
    email = StringField('Email', validators=[
        DataRequired(),
        Email("Must be a valid email address.")
    ], render_kw={'placeholder': 'example@email.com'})
    # TODO: Ask about using flask-change-password instead of changing password on this page:
    #  https://pypi.org/project/flask-change-password/
    submit = SubmitField('Save')

    # Prevents duplicate accounts
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).one_or_none()
        if existing_user:
            raise ValidationError('Email address already registered.')

    def validate_password(self, password):
        # Consider adding special character requirements
        if not any(c.isalpha() for c in password.data) or not any(c.isdigit() for c in password.data):
            raise ValidationError('Password must contain at least one letter and one digit.')
