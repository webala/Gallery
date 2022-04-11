from tokenize import String
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    email =StringField('Email Address', validators=[Email(), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ChangeProfilePictureForm(FlaskForm):
    new_picture = FileField('New picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    change_picture = SubmitField('Change Profile Picture')

class AddArtWork(FlaskForm):
    art_work = FileField('Choose Art to Upload', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    name = StringField('Name Your Art', validators=[DataRequired(), Length(min=2, max=20)])
    description = TextAreaField('Describe Your Art', validators=[DataRequired(), Length(min=2, max=100)])
    add_art = SubmitField('All Done')
