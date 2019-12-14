from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app import bcrypt
from app.dbclass import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20), 
                           Regexp(r'^\w+$', message='Only alphanumeric characters are allowed.')])
    firstname = StringField('First Name', validators=[DataRequired(), 
                           Regexp(r'^[a-zA-Z]+$', message='Only letters are allowed.')])
    lastname = StringField('Last Name', validators=[DataRequired(), 
                           Regexp(r'^\w+$', message='Only lettters are allowed.')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), 
                           Regexp(r'^\S+$', message='White spaces are not allowed.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please select another.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Either use another email id or login using the correct credential.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=4, max=20), 
                           Regexp(r'^\w+$', message='Only alphanumeric characters are allowed.')])
    firstname = StringField('First Name', validators=[DataRequired(),
                           Regexp(r'^[a-zA-Z]+$', message='Only lettters are allowed.')])
    lastname = StringField('Last Name', validators=[DataRequired(), 
                           Regexp(r'^[a-zA-Z]+$', message='Only lettters are allowed.')])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    new_password = PasswordField('New Password')
    confirm_new_password = PasswordField('Confirm New Password',
                                     validators=[EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(email=username.data).first()
            if user:
                raise ValidationError(f'Username already exists. Please select another.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(f'Email already exists. Please select another email')

    def validate_password(self, new_password):
        if new_password != '' and ' ' in new_password:
            raise ValidationError('The password cannot contain white space.')

class SearchForm(FlaskForm):
    text = StringField('Search Text', validators=[DataRequired()])
    submit = SubmitField('Search')