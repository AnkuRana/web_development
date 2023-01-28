from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, InputRequired, Length
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .db_models import User, Notes

class Signup_form(FlaskForm):
    first_name = StringField("First Name",validators=[DataRequired()])
    last_name = StringField("Last Name",validators=[DataRequired()])
    email = EmailField("Email",validators=[InputRequired(), Email(message="please enter correct email format.")])
    password = PasswordField("Password",validators=[InputRequired(), Length(min=8, message="Password must conatin min 8 letters."), EqualTo("password_cnf", message="Passwords must match.")])
    password_cnf = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Register")

class Login_form(FlaskForm):
    email = EmailField("Email",validators=[InputRequired()])
    password = PasswordField("Password",validators=[InputRequired()])
    submit = SubmitField("Login")


auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = Login_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("logged in successfully!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect passowrd!", category="error")
        else:
            flash("Email does not exist!", category="error")

        
    return render_template("login.html",form=form, user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
    form = Signup_form()
    if form.validate_on_submit():
        firstname = form.first_name.data
        lastname = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists!", category="error")
        else:
            new_user = User(email=email, firstname=firstname,lastname=lastname, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully created", category="success")
            login_user(new_user)
            return redirect(url_for("views.home"))
 
    return render_template("register.html",form=form)

@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

# @auth.route("/", methods=["GET", "POST"])
# def home():
#     return "<h1>Home Page</h1>"