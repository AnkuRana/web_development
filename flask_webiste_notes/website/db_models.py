from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstname =  db.Column(db.String(150))
    lastname = db.Column(db.String(150), nullable=False)
    notes = db.relationship("Notes")

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
