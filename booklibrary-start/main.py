from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os import path

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


def check_db():
    is_exist = path.exists("./instance/books_collection.db")
    return is_exist

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True, nullable=False)
    author = db.Column(db.String(200), nullable=False)
    rating  = db.Column(db.String(50), nullable=False)

with app.app_context():
               db.create_all()

# if not check_db:
#     with app.app_context():
#         db.create_all()
#         print("true")
# else:
#     print("false")



@app.route('/')
def home():
    is_lib_empty = False
    all_books = db.session.query(Book).all()
    if all_books == []:
        is_lib_empty = True
    return render_template("index.html", books=all_books, lib_empty=is_lib_empty)


@app.route("/add", methods=["POST", "GET"])
def add():
    data = request.form
    if request.method == "POST":
        book=data["book_name"] 
        author=data["author"] 
        rating=data["rating"]
        book_details = Book(title=book, author=author, rating=rating)
        with app.app_context():
            db.session.add(book_details)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    data = request.form
    if request.method == "POST":
        book_id = data["id"]
        book = Book.query.get(book_id)
        book.rating = data["rating"]
        db.session.commit()
        return redirect(url_for("home"))
    book_no = request.args.get('book_id')
    book_selected = Book.query.get(book_no)
    return render_template("edit.html",book=book_selected)

@app.route("/delete")
def delete():
    book_id = request.args.get("book_id")
    book_selected = Book.query.get(book_id)
    db.session.delete(book_selected)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/test/<int:book_id>")
def test(book_id):
    return f"<h1>{book_id}</h1>"

if __name__ == "__main__":
    app.run(debug=True)

