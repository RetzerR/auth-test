from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify
from replit import db
import uuid
app = Flask('app')


try:
    db["users"]
    db["ids"]
    db["userids"]
except KeyError:
    db["users"] = {}
    db["ids"] = {}
    db["userids"] = {}

@app.route("/signup/", methods=["POST"])
def user():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username in db["users"]:
        db["users"][username] = password
        id_ = str(uuid.uuid4())
        db["ids"][username] = id_
        db["userids"][id_] = username
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
            resp.set_cookie("user", db["ids"][username])
            return resp
        else:
            return redirect("/?login=1&response=2")
    else:
        return redirect("/?login=1&response=1")

@app.route("/username/", methods=["GET"])
def username():
    try:
        return db["userids"][request.args.get("id")]
    except: return "ERROR: USER NOT FOUND"

app.run(host='0.0.0.0', port=8080)