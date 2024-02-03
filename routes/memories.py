from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db, storage
from datetime import datetime

blueprint = Blueprint(
    'memories', 
    __name__
)

@blueprint.route('/')
def home():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    keys = db.reference("bucket").get()

    if keys:
        keys = keys.keys()

    else:
        keys = []

    bucket = []

    for key in keys:
        bucket.append(
            db.reference(f"bucket/{key}").get()
        )
    
    return render_template("bucket/home.html", bucket=bucket)
    
@blueprint.route('/create', methods=["GET", "POST"])
def create():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        memories = db.reference("memories").get()

        if memories:
            memories = memories.keys()

        else:
            memories = []
            
        return render_template("memories/create.html")
    
    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        memories = db.reference("bucket")

        memories.push({
            "title": title,
            "description": description,
            "date": date
        })

        return redirect("/memories")
    
@blueprint.route('/upload', methods=["GET", "POST"])
def upload():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        memories = db.reference("memories").get()

        if memories:
            memories = memories.keys()

        else:
            memories = []
        
        return render_template("memories/upload.html", memories=memories)
    
    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        memories = db.reference("memories")

        memories.push({
            "title": title,
            "description": description,
            "date": date
        })

        return redirect("/memories")