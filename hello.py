from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Change display another time</p>"

@app.route("/user/<username>")
def user(username):
    return f'<h1>Username: {username} </h1>'