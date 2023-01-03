from flask import Flask, render_template
import requests

dummpy_data_api = "https://api.npoint.io/a0435bd3cd577072ef68"

def get_dummy_blogpost(rest_api):
    response =  requests.get(rest_api)
    response.raise_for_status()
    response = response.json()
    return response

blog_data = get_dummy_blogpost(dummpy_data_api) 

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html", data=blog_data)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/<int:index>")
def post_view(index):
    view_post = None
    for post in blog_data:
        if post['id'] == index:
            view_post = post
    return render_template("post.html",post=view_post)



if __name__ == "__main__":
    app.run(debug=True)
