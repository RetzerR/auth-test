from flask import Flask, render_template, request, redirect, url_for, make_response
from replit import db
app = Flask('app')


try:
    db["users"]
except KeyError:
    db["users"] = {}

@app.route("/signup/", methods=["POST"])
def user():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username in db["users"]:
        db["users"][username] = password
        return redirect("/?login=1&signedup=1")
    else:
        return redirect("/?login=3")

@app.route('/')
def hello_world():
  return render_template("index.html")

@app.route("/logout/")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie("user", expires=0)
    return resp

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in db["users"]:
        if password == db["users"][username]:
            resp = make_response(redirect("/"))
            resp.set_cookie("user", username)
            return resp
        else:
            return redirect("/?login=1&response=2")
    else:
        return redirect("/?login=1&response=1")

app.run(host='0.0.0.0', port=8080)