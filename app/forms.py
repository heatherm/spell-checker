from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id="uname")
    two_factor = StringField('Two Factor', validators=[DataRequired()], id="2fa")
    password = PasswordField('Password', validators=[DataRequired()], id="pword")
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], id="uname")
    password = PasswordField('Password', validators=[DataRequired()], id="pword")
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
