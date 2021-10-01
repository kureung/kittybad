from flask import Flask, render_template, request, url_for, redirect
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("door.html")


@app.route("/regions", methods=['GET'])
def move_regions():
    return render_template("regions.html")


@app.route("/login", methods=['GET'])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
