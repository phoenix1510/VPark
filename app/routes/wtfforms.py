from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField , HiddenField
from wtforms.validators import DataRequired, InputRequired, Length , Email , EqualTo


# -- auth forms --
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


# -- admin forms -- 

class Add_Fal_Form(FlaskForm):
    name = StringField('Facility Name', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired(),Length(min=10 , max=500)])
    submit = SubmitField("Add facility")
class Remove_fal_Form(FlaskForm):
    facility_id = HiddenField('facility_id',validators=[InputRequired()])
    submit = SubmitField('Remove')

class Edit_fal_Form(FlaskForm):
    facility_id = HiddenField('Facility_id',validators=[InputRequired()])
    name = StringField('New Name', validators=[DataRequired()])
    address = TextAreaField('New Address', validators=[DataRequired(),Length(min=10 , max=500)])
    submit = SubmitField("Edit facility")
class Add_Flo_Form(FlaskForm):
    floor_number = IntegerField('Floor Number', validators=[DataRequired()])
    submit = SubmitField("Add Floor")

class Remove_Flo_Form(FlaskForm):
    floor_id = HiddenField('floor_id', validators=[InputRequired()])
    submit = SubmitField("Remove floor")

class Add_slo_Form(FlaskForm):
    slot_number = IntegerField('Slot Number', validators=[DataRequired()])
    submit = SubmitField('Add slot')

class Remove_slo_Form(FlaskForm):
    slot_id = HiddenField("slot_id", validators=[InputRequired()])
    submit = SubmitField('Remove slot')

class Edit_status_Form(FlaskForm):
    slot_id = HiddenField("slot_id", validators=[InputRequired()])
    status = StringField("New Status", validators=[DataRequired()])
    submit = SubmitField('Edit Status')

class Add_Rate_Form(FlaskForm):
    vehicle_type = StringField('Vehicle Type', validators=[DataRequired(), Length(max=50)])
    rate_per_hour = IntegerField('Rate per Hour (₹)', validators=[DataRequired()])
    submit = SubmitField('Add Rate')

class Remove_Rate_Form(FlaskForm):
    rate_id = HiddenField('rate_id', validators=[InputRequired()])
    submit = SubmitField('Remove')