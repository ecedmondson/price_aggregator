from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignUpForm(FlaskForm):
    fname = StringField('First Name', validators=[
        DataRequired(message='Please enter first name')])
    lname = StringField('Last Name', validators=[
        DataRequired(message='Please enter last name')])
    email = StringField('Email', validators=[
        Email(message='Not a valid email address.'),
        DataRequired(message='Please enter an email.')])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter a password'),
        Length(min=8, message='Password must be at least 8 characters')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        Email(message='Not a valid email address.'),
        DataRequired(message='Please enter an email.')])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter a password')])
    submit = SubmitField('Login')