from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import data_required, Email, length
from flask_bootstrap import Bootstrap

class Loginform(FlaskForm):
    email = StringField(label="Email", validators=[data_required(), Email()])
    password = PasswordField(label="Password", validators=[data_required(), length(min=8)])
    submit = SubmitField(label="Log in")


app = Flask(__name__)
Bootstrap(app)
app.secret_key = "sdkjuahsdjkhas"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    f_form = Loginform()
    if f_form.validate_on_submit():
        if f_form.email.data == "amitrana.com007@yahoo.com" and f_form.password.data=="12345678":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=f_form)

# @app.route("/success")
# def success():
#     return render_template("success.html")

# @app.route("/denied")
# def denied():
#     return render_template("denied.html")

if __name__ == '__main__':
    app.run(debug=True)