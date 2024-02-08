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

            db.reference('auth').update({token: user})

            db.reference(f"users/{user}/sessions/{token}").update({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "active": True,
                "ip": request.remote_addr
            })

            session["token"] = token

            return redirect("/")
        
        else: 
            return "Incorrect Password"
        
@blueprint.route('/logout')
def logout():
    token = session.get("token")

    authorized = db.reference(f'auth/{token}').get()

    if authorized:
        db.reference('auth').update({
            token: None
        })

    db.reference(f'users/{authorized}/sessions/{token}').update({"active": False})

    session["token"] = None

    return redirect("/")

@blueprint.route("/sessions")
def sessions():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    sessions = db.reference(f"users/{authorized}/sessions").get()

    if sessions:
        sessions = sessions.values()

    return render_template("auth/sessions.html", sessions=sessions)