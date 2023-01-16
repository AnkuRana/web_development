# import sqlite3 as sql

# db = sql.Connection("books_collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_collection_2.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String)
    author = db.Column(db.String)
    rating  = db.Column(db.String)

# book2 = Book(bookname="sdaksd", author="asaasd", rating="9.9")
with app.app_context():
    db.create_all()
   

