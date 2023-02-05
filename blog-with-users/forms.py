from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField
from wtforms.validators import DataRequired, URL, Email, InputRequired, EqualTo, Length
from flask_ckeditor import CKEditorField

##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class RegisterForm(FlaskForm):
    email = EmailField(validators = [DataRequired(), Email()])
    password = PasswordField(validators = [InputRequired(), Length(min=6), EqualTo("password_cnf", message="Password must match.")])
    password_cnf = PasswordField("Confirm Password", validators = [InputRequired()])
    submit = SubmitField("Sign-Up")

class LoginForm(FlaskForm):
    email = EmailField(validators = [DataRequired(), Email()])
    password = PasswordField(validators = [InputRequired()])
    submit = SubmitField("Sign-in")

