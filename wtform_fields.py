from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError



class RegistrationForm(FlaskForm):
    ''' Registration Form '''

    username = StringField('username_label', validators=[InputRequired(message="Username required"), Length(min=4, max=25, message="Username must be between 4 and 25 character")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), Length(min=4, max=25, message="Password must be between 4 and 25 character")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Password required"), EqualTo('password', message='Password must match')])

    submit_button = SubmitField('Create')