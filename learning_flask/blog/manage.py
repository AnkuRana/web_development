from main import app, User, db, Blogpost, Comment, Tag, blogpost_tag, migrate


@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app, 
        db=db, 
        User=User, 
        BlogPost=Blogpost, 
        Comment=Comment,
        Tag=Tag,
        blogpost_tag=blogpost_tag,
        migrate=migrate
        )