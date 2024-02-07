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
    
    data = db.reference("bucket").get()

    bucket = []

    if data:
        for key in data.keys():
            bucket.append(
                data[key]
            )

            bucket[-1]["uid"] = key

    return render_template("bucket/home.html", bucket=bucket)
    
@blueprint.route('/view/<uid>', methods=["GET", "POST"])
def view(uid):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    fish = db.reference(f"bucket/{uid}").get()

    if not fish:
        return redirect("/404")
    
    fish["uid"] = uid
    
    return render_template("bucket/view.html", fish=fish)

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
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "by": by
        })

        return redirect("/bucket")
    
@blueprint.route('/delete/<uid>', methods=["GET", "POST"])
def delete(uid):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    fish = db.reference(f"bucket/{uid}")

    if not fish.get():
        return redirect("/404")
    
    fish.set({})

    return redirect("/bucket")