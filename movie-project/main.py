from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, URLField, TextAreaField, FloatField
from wtforms.validators import DataRequired
import get_movies as movie_api
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie_collection.db"
db = SQLAlchemy(app)
Bootstrap(app)

def check_db():
    is_db_exists = path.exists("./instance/movie_collection.db")
    return is_db_exists



class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review= db.Column(db.String(100))
    img_url= db.Column(db.String(100), nullable=False)
    plot_summary = db.Column(db.String(2000))
    author = db.Column(db.String(200))
    vedio_type = db.Column(db.String(100))
    imdb_toprank = db.Column(db.String(50))
    imdb_rating = db.Column(db.String(50))
    genre = db.Column(db.String(500))


class Movie_Form(FlaskForm):
    movie_title = StringField("Movie Title")
    # movie_year = StringField("Enter movie year")
    # movie_description = TextAreaField("Enter the movie description")
    # movie_rating = FloatField("rate the movie")
    # movie_ranking = IntegerField("Enter movie rank")
    # movie_review = TextAreaField("Enter the movie review")
    # movie_img_url= URLField("Enter the movie image url")
    submit = SubmitField("Add Movie")

class Edit_Form(FlaskForm):
    rating = FloatField("Rate the move out of 10 e.g 7.2/10")
    review = StringField("Waht do you thought about the move!")
    update = SubmitField("update")

if not check_db():
    with app.app_context():
        db.create_all()



@app.route("/")
def home():
    all_movies = db.session.query(Movies).all()
    is_list_empty = False
    if all_movies == []:
        is_list_empty = True
    else:
        all_movies = Movies.query.order_by(Movies.rating).all()
        for i in range(len(all_movies)):
            all_movies[i].ranking = len(all_movies) - i
        db.session.commit()
    return render_template("index.html", movies=all_movies, list_empty=is_list_empty)

@app.route("/add", methods=["POST", "GET"])
def add_movie():
    form = Movie_Form()
    if form.validate_on_submit():
        movie_name = form.movie_title.data
        movies_list = movie_api.get_movie(movie_name, movie_api.headers)
        # new_movie = Movies(
        #     title = form.movie_title.data,
        #     year = form.movie_year.data,
        #     description = form.movie_description.data,
        #     rating = form.movie_rating.data,
        #     ranking = form.movie_ranking.data,
        #     review = form.movie_review.data,
        #     img_url = form.movie_img_url.data
        #     )
        # db.session.add(new_movie)
        # db.session.commit()
        return render_template("select.html", movie_list=movies_list)
    return render_template("add.html", form=form)


@app.route("/select", methods=["POST","GET"])
def select_movie():
    if request.method == "GET":
        movie_id = request.args.get("movie_id")
        movie_data = movie_api.get_movie_details(movie_id, movie_api.headers)
        new_movie = Movies(
            title = movie_data["title"],
            year = movie_data["year"],
            rating = 0,
            description = movie_data["plot_outline"],
            imdb_rating = movie_data["rating"],
            imdb_toprank = movie_data["toprank"],
            vedio_type = movie_data["type"],
            img_url = movie_data["image"],
            review = "Review ",
            genre = movie_data["genres_list"],
            plot_summary = movie_data["plot_summary"],
            author = movie_data["author"]
            )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("select.html")

@app.route("/edit", methods=["POST","GET"])
def edit_movie():
    form = Edit_Form()
    movie_key = request.args.get("movie_id")
    selected_movie = Movies.query.get(movie_key)
    print(selected_movie.title)
    if form.validate_on_submit():
        selected_movie.rating = form.rating.data
        selected_movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie=selected_movie, form=form)

@app.route("/delete", methods=["POST","GET"])
def delete_movie():
    movie_key = request.args.get("movie_id")
    selected_movie = Movies.query.get(movie_key)
    db.session.delete(selected_movie)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
