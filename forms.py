from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, validators, ValidationError
from wtforms.validators import InputRequired, Length, Email

class CreateForm(FlaskForm):
    username = StringField("Username :" , validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password :", validators=[InputRequired()])
    email = EmailField("Email Address :", validators=[InputRequired(), Email(), Length(max=50)])
    first_name = StringField("First Name :", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name ;", validators=[InputRequired(), Length(max=30)])


class Log_in(FlaskForm):
    username = StringField("Username :" , validators=[InputRequired(), Length(max=20)])
    password = PasswordField("Password :", validators=[InputRequired()])

class FeedbackForm (FlaskForm):
    title = StringField("Title :", validators=[InputRequired(), Length(max=100)] )
    content = StringField("Content", validators=[InputRequired()])

class UpdateFeedbackForm (FlaskForm):
    title = StringField("Title :", validators=[ Length(max=100)] )
    content = StringField("Content", )

    