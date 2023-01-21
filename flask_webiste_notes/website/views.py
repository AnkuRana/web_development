from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from .db_models import Notes
from . import db

views = Blueprint("views", __name__)

class Note_form(FlaskForm):
    note =  TextAreaField("",validators=[DataRequired()])
    submit = SubmitField("Add Note")

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    form = Note_form()
    if form.validate_on_submit():
        note = form.note.data
        new_note = Notes(note_data=note, user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash("Note added!", category="success")
        return redirect(url_for("views.home"))
    return render_template("home.html",form=form, user=current_user)

@views.route("/delete", methods=["GET", "POST"])
@login_required
def delete_note():
    note_id = request.args.get("note_id")
    selected_note = Notes.query.get(note_id)
    db.session.delete(selected_note)
    db.session.commit()
    return redirect(url_for("views.home"))