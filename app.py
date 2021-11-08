"""
Simple "Hello, World" application using Flask
"""
from flask import Flask, render_template, request
from mbta_helper import find_stop_near


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/hello/")
def hello(name=None):
    if name:
        name = name.upper()
        return render_template("hello.html", name=name)
    return "Hello"

@app.route("/mbta/", methods=["GET", "POST"])
def get_nearest_station():
    if request.method == "POST":
        place = float(request.form["a"])
        nearest = find_stop_near(place)
        if nearest:
            return render_template("Nearest_MBTA.html" , 
            place=place, 
            nearest=nearest,)
        else: 
            return render_template("MBTA_form.html", 
            error = True)
    return render_template("MBTA_form.html", error=None)

if __name__ == '__main__':
    app.run(debug=True)
