from flask import Blueprint, render_template
from extensions import db
from config import DevConfig
from sqlalchemy.sql import func
from models import Blogpost, User, blogpost_tag, Tag, Comment

auth = Blueprint("auth",__name__)

def get_data():
    recent = db.session.execute(db.select(Blogpost).order_by(Blogpost.publish_date.desc()).limit(5).all())
    # recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.execute(db.select(Tag, func.count(blogpost_tag.c.post_id).label('tag_count'))).join(blogpost_tag).group_by(Tag).order_by('tag_count DESC').limit(5).all()
    return recent, top_tags



@auth.route('/<int:page>')
def home(page=1):
    posts = db.paginate(db.select(Blogpost).order_by(Blogpost.publish_date.desc()),page=page,per_page=DevConfig.POSTS_PER_PAGE, error_out=False)
    recent , top_tags =  get_data()
    return render_template("index.html", posts=posts, recent=recent, top_tags=top_tags)

@auth.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = db.get_or_404(Blogpost, post_id)
    return render_template("post.html")

@auth.route('/posts_by_tag/<string:tag_name>', methods=['GET', 'POST'])
def posts_by_tag(tag_name):
    tag = db.one_or_404(db.session.execute(db.select(User).filter_by(name=tag_name)))
    

@auth.route('/posts_by_user/<string:user_name>', methods=['GET', 'POST'])
def posts_by_user(user_name):
    user = db.first_or_404(db.session.execute(db.create_allselect(User).filter_by(username=user_name)))
    posts = db.session.execute(db.select(Blogpost).filter_by(user_id=user.id))
    recent, top_tags = get_data()
    return render_template("user_posts.html", user=user,posts=posts, recent=recent, top_tags=top_tags)
