from flask import Flask, render_template, request, redirect, url_for
from replit import db
app = Flask('app')

try:
    db["users"]
except KeyError:
    db["users"] = {}

@app.route("/user/")
def user():
    db["users"][request.args.get("username")] = request.args.get("password")
    return redirect("/")

@app.route('/')
def hello_world():
  return render_template("index.html")

@app.route("/logout/")
def logout():
    return render_template("logout.html", user=request.args.get("user"))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in db["users"]:
        if password == db["users"][username]:
            return render_template("login.html", user=username)
        else:
            return "wrong password"
    else:
        return "no user found"

app.run(host='0.0.0.0', port=8080)