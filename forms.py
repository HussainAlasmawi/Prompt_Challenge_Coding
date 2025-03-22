from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    destination = SelectField('Destination', choices=[], validators=[DataRequired()])
    departure_date = SelectField('Departure Date', choices=[], validators=[DataRequired()])
    seat_class = SelectField('Seat Class', choices=[('Economy', 'Economy'), ('Luxury', 'Luxury'), ('VIP', 'VIP Zero-Gravity')], validators=[DataRequired()])
    submit = SubmitField('Book Trip')
