from flask import Flask, render_template, request
import smtplib, os, requests
import datetime as dt


MY_EMAIL = "ankurana.com007@gmail.com"
MYAPPPASSWORD = os.environ.get("EMAIL_PASS")
dummpy_data_api = "https://api.npoint.io/a0435bd3cd577072ef68"

def get_dummy_blogpost(rest_api):
    response =  requests.get(rest_api)
    response.raise_for_status()
    response = response.json()
    return response

def send_email(email, message):
    # print(message)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MYAPPPASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,
                            to_addrs=MY_EMAIL,
                            msg=f"Subject:contact from blog!\n\n{message}".encode("utf8"))


blog_data = get_dummy_blogpost(dummpy_data_api) 

app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template("index.html", data=blog_data)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    data = request.form
    print(data)
   
    if request.method == "POST":
        message = f"name: {data['fullname']}\nemail :{data['email']}\nmobile_no:{data['phone']}\nmessage:{data['message']}"
        send_email(MY_EMAIL, message)
        return render_template("contact.html", msg_send=True)
    return render_template("contact.html", msg_send=False)


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

# @app.route("/form-entry" , methods=["POST", "GET"])
# def recieve_data():
#     if request.method == "POST":
#         return "<h1>Successfully sent your message.</h1>"
#     else:
#         return "Error occurred."


if __name__ == "__main__":
    app.run(debug=True)
