from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from os import path

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"You are successfully logged in."
login_manager.login_message_category = "info"
login_manager.init_app(app)



##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __repr__(self) -> str:
        return f"email: {self.email} \n\n"
#Line below only required once, when creating DB. 
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(select(User).where(User.id == int(user_id))).scalar()

@app.route('/')
@login_required
def home():
    return render_template("index.html", user=current_user)


@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        data = request.form
        user = db.session.execute(select(User).where(User.email==data["email"])).scalar()
        if user:
            flash("Email already exists!", category="error")
        else:
            new_user = User(
                email=data["email"], 
                password=generate_password_hash(data["password"], method="pbkdf2:sha256", salt_length=8), 
                name=data["name"]
                )
            db.session.add(new_user)
            db.session.commit()
            flash("Account successfully created", category="success")
            login_user(new_user)
            return redirect(url_for("secrets"))   
    return render_template("register.html",user=current_user)


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        data = request.form
        user = db.session.execute(select(User).where(User.email==data["email"])).scalar()
        print(user)
        # user = User.query.filter_by(email=data["email"]).first()
        if user:
            if check_password_hash(user.password, data["password"]):
                login_user(user)
                flash("logged in successfully 9!", category="success")
                return redirect(url_for("secrets"))
            else:
                flash("Incorrect passowrd!", category="error")
        else:
            flash("Email does not exist!", category="error")
    return render_template("login.html", user=current_user)


@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/download')
@login_required
def download():
    return send_from_directory("static","files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)
