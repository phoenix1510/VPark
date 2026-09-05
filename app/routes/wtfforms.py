from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length , Email , EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=4, max=20)])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=4, max=20),EqualTo('confirm',message='Passwords must match!')])
    confirm = PasswordField('Repeat Password')
    phone_number = StringField('Phone number', validators=[DataRequired(),Length(min=10, max=12)])
    submit = SubmitField("Register")