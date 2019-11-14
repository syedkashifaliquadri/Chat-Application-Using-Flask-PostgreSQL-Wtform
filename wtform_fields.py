from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, EqualTo, ValidationError
from models import User


def invalid_credentials(form, field):
    """ User n Pass Checker """

    username_entered = form.username.data
    password_entered = field.data

    #check credential are valid
    user_object = User.query.filter_by(username= username_entered).first()
    if user_object is None:
        raise ValidationError("Username or pass incorrect")
    elif password_entered != user_object.password:
        raise ValidationError("Username or pass incorrect")


class RegistrationForm(FlaskForm):
    ''' Registration Form '''

    username = StringField('username_label', validators=[InputRequired(message="Username required"), 
                          Length(min=4, max=25, message="Username must be between 4 and 25 character")])

    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), 
                            Length(min=4, max=25, message="Password must be between 4 and 25 character")])

    confirm_pswd = PasswordField('confirm_pswd_label', validators=[InputRequired(message="Password required"), 
                                EqualTo('password', message='Password must match')])

    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username= username.data).first()
        if user_object:
            raise ValidationError("Username already exists. Select different username.")

class LoginForm(FlaskForm):
    """ Login form """
    username = StringField('username_label', validators=[InputRequired(message="Username required")])
    password = PasswordField('password_label', validators=[InputRequired(message="Password required"), invalid_credentials])
    submit_button = SubmitField('Login')

