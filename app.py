"""
Simple "Hello, World" application using Flask
"""
from flask import Flask, render_template, request
from mbta_helper import find_stop_near


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/mbta/")
def hello(name=None):
    if name:
        name = name.upper()
        return render_template("hello.html", name=name)
    return "Hello"



if __name__ == '__main__':
    app.run(debug=True)
