from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime
from json import loads
from uuid import uuid4
from os import path, getcwd

blueprint = Blueprint(
    'auth', 
    __name__
)
    
@blueprint.route('/login', methods=["GET", "POST"])
def login():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if authorized:
        return redirect("/todos")
    
    if request.method == "GET":
        return render_template("auth/login.html")
        
    elif request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        with open(path.join(getcwd(),"config/auth.json"), "r") as file:
            auth = loads(file.read())

        if auth[user] == password:
            token = str(uuid4())

            ref = db.reference('auth')

            ref.update({token: {
                "time": datetime.now().timestamp(),
                "user": user
            }})

            session["token"] = token

            return redirect("/bucket")
        
        else: 
            return "Incorrect Password"
        
@blueprint.route('/logout')
def logout():
    ref = db.reference('auth')

    ref.update({session["token"]: None})

    session["token"] = None

    return redirect("/")