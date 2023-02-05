from flask import Flask, render_template, redirect, url_for, flash , request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"You are successfully logged in."
login_manager.login_message_category = "info"
login_manager.init_app(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(select(Person).where(Person.id == int(user_id))).scalar()


##CONFIGURE TABLES
class Person(UserMixin, db.Model):
     id = db.Column(db.Integer, primary_key=True)
     email = db.Column(db.String(250), nullable=False, unique=True)
     password = db.Column(db.String(250), nullable=False)
     my_blogposts = db.relationship("Post")

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("person.id"))

with app.app_context():
    db.create_all()

# create admin only decorator
def adminonly(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id !=1:
            return abort(403)
        #or continue with the route function
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def get_all_posts():
    posts = Post.query.all()
    return render_template("index.html", all_posts=posts, user=current_user)



@app.route("/register", methods=["GET", "POST"])
def register():
    form =  RegisterForm()
    if form.validate_on_submit():
        user = db.session.execute(select(Person).where(Person.email == form.email.data)).scalar()
        if user:
            flash("User Already exists.", category="info")
            return redirect( url_for("login") )
        else:
            new_user = Person(email=form.email.data , 
                            password=generate_password_hash(form.password.data, 
                                    method='pbkdf2:sha256',
                                    salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully.", category="info")
            login_user(new_user)
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=form,user=current_user)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(select(Person).where(Person.email == form.email.data)).scalar()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("login successfull", category="success")
            return redirect(url_for("get_all_posts"))
        else:
            flash("login failed! Invalid Credentials.", category="error")
    return render_template("login.html", form=form, user=current_user)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = Post.query.get(post_id)
    return render_template("post.html", post=requested_post, user=current_user)


@app.route("/about")
def about():
    return render_template("about.html",user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)


@app.route("/new-post", methods=["POST", "GET"])
@login_required
@adminonly
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user.email.split(".")[0],
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, user=current_user)


@app.route("/edit-post/<int:post_id>")
@login_required
@adminonly
def edit_post(post_id):
    post = Post.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, user=current_user)


@app.route("/delete/<int:post_id>")
@login_required
@adminonly
def delete_post(post_id):
    post_to_delete = Post.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(debug=True)
