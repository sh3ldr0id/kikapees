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
    
    data = db.reference("memories").get()
    
    keys = []

    if data:
        keys = data.keys()

    memories = []

    for key in keys:
        memories.append(
            data[key]
        )
    
    return render_template("memories/home.html", memories=memories)
    
@blueprint.route('/create', methods=["GET", "POST"])
def create():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        return render_template("memories/create.html")
    
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
    
@blueprint.route('/upload', methods=["GET", "POST"])
def upload():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        memories = db.reference("memories").get()

        keys = []

        if memories:
            keys = memories.keys()
        
        titles = []

        for key in keys:
            titles.append(
                memories[key]["title"]
            )
        
        return render_template("memories/upload.html", titles=titles)
    
    elif request.method == "POST":
        title = request.form["title"]
        files = request.files.getlist("file")

        uid = db.reference("memories").order_by_child("title").equal_to(title).get().keys()
        uid = list(uid)[0]

        for file in files:

            suffix = 1

            filename = file.filename
            extension = filename.rsplit('.', 1)[1]

            while storage.bucket("kikapees.appspot.com").blob(f"{title}/{filename}").exists():
                suffix += 1
                filename = f'{filename} ({suffix}).{extension}'

            db.reference(f"memories/{uid}/files").push({
                "filename": filename,
                "uploadedOn": datetime.now().timestamp()
            })

            blob = storage.bucket("kikapees.appspot.com").blob(f"{title}/{filename}")

            blob.upload_from_file(file)

        return redirect("/memories")