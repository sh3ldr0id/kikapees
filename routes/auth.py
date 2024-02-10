from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime
from json import loads
from uuid import uuid4
from os import path, getcwd
import requests

blueprint = Blueprint(
    'auth', 
    __name__
)

def get_location(ip_address):
    try:
        response = requests.get(f'https://api.iplocation.net/?ip={ip_address}').json()

        location_data = {
            "city": response.get("city"),
            "region": response.get("region"),
            "country": response.get("country_name")
        }
    except:
        location_data = {}

    return location_data
    
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

            location = get_location(request.remote_addr)

            print(location)

            db.reference(f"users/{user}/sessions/{token}").update({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "active": True,
                "ip": request.remote_addr,
                "location": location
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

@blueprint.route('/deactivate/<tok>')
def deactivate(tok):
    token = session.get("token")

    authorized = db.reference(f'auth/{token}').get()

    if authorized:
        db.reference('auth').update({
            tok: None
        })

    db.reference(f'users/{authorized}/sessions/{tok}').update({"active": False})

    return redirect("/auth/sessions")

@blueprint.route('/delete/<tok>')
def delete(tok):
    token = session.get("token")

    authorized = db.reference(f'auth/{token}').get()

    if authorized:
        db.reference('auth').update({
            tok: None
        })

    db.reference(f'users/{authorized}/sessions').update({tok: None})

    return redirect("/auth/sessions")

@blueprint.route("/sessions")
def sessions():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    sessions = db.reference(f"users/{authorized}/sessions").order_by_child("time").get()

    if sessions:
        tokens = list(sessions.keys())
        sessions = list(sessions.values())

        for index in range(len(sessions)):
            sessions[index]["active"] = "Active" if sessions[index]["active"] else "Inactive"
            sessions[index]["token"] = tokens[index]

    sessions.reverse()

    return render_template("auth/sessions.html", sessions=sessions)