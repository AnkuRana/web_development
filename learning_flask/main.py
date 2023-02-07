from flask import Flask
from config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import select
from sqlalchemy.sql import func


app = Flask(__name__)
app.config.from_object(DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(350), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship("Blogpost", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"id:{self.id} | UserName:{self.username} | email:{self.email}."


blogpost_tag = db.Table("blogpost_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("blogpost.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"))
)

class Blogpost(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    subtitle = db.Column(db.String(500), nullable=False)
    body = db.Column(db.Text())
    publish_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="blogpost", lazy="dynamic")
    has_tags = db.relationship("Tag", secondary=blogpost_tag, backref="has_posts")

    def __repr__(self) -> str:
        return f"BlogPost- id:{self.id} | title:{self.title} | user_id:{self.user_id}."

class Tag(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

    def __repr__(self) -> str:
        return f"Tag: {self.name}."



class Comment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    content = db.Column(db.Text())
    comment_by = db.Column(db.String(250), nullable=False, default="anonymous")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey("blogpost.id"))

    def __repr__(self) -> str:
        return f"Comment- id:{self.id} | title:{self.content} | post_id:{self.post_id}."
    
def sidebar_data():
    recent = db.session.execute(select(Blogpost).order_by(Blogpost.publish_date.desc()).limit(5).all())
    # recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.execute(select(Tag, func.count(blogpost_tag.c.post_id).label('tag_count'))).join(blogpost_tag).group_by(Tag).order_by('tag_count DESC').limit(5).all()
    return recent, top_tags


@app.route('/')
def home():
    return "<h1>Hello World!!!. </h1>"

if __name__ == "__main__":
    app.run()