from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime

blueprint = Blueprint(
    'bucket', 
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
        return render_template("bucket/create.html")
    
    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        by = authorized["user"]

        bucket = db.reference("bucket")

        bucket.push({
            "title": title,
            "description": description,
            "created": str(datetime.now()),
            "by": by
        })

        return redirect("/bucket")