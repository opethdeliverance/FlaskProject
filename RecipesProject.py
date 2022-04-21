from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "sup"

@app.route("/stev")
def steve_name():
    return "hello, steve!"

@app.route("/<string:name>")
def hello_name(name):
    name = name.capitalize()
    return f"hello, {name}"
