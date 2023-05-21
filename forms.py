from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    """Form for registering user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[Email(), 
                                             Length(max=50), 
                                             InputRequired()])
    first_name = StringField("First name", validators=[Length(max=30),
                                                       InputRequired()])
    last_name = StringField("Last name", validators=[Length(max=30),
                                                       InputRequired()])

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """feedback form."""

    title = StringField("Title", validators=[InputRequired(),
                                             Length(max=100)]
                                             )
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Leave blank."""