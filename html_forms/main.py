from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def recieved_data():
    error="none"
    if request.method == "POST":
        return f"hello post {request.method} <h1>username:  {request.form['fname']} password: {request.form['password']}</h1>"
    else:
        return f"fnane: {request.args.get('fname')}"
 
if __name__ == "__main__":
    app.run(debug=True)
