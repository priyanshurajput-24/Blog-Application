from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField


# create a Search Form
class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Submit")



# create a Post Form
class PostForms(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    author = StringField("Author")
    key_note = StringField("key_note", validators=[DataRequired()])
    submit = SubmitField("Submit") 


# create a Login Form 
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# create a Comment Form
class CommentForm(FlaskForm):
    text = StringField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit")



# create a User Form
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    about_user = TextAreaField("About User")
    profile_pic = FileField("Profile Pic")
    hashed_password = PasswordField('Password', validators=[DataRequired(), EqualTo('hashed_password2')])
    hashed_password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField("Submit")

