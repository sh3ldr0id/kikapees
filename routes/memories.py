from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db, storage
from datetime import datetime
from uuid import uuid4

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
        pfp = request.files.get("pfp")
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        if pfp:
            extension = pfp.filename.rsplit('.', 1)[1]

            blob = storage.bucket("kikapees.appspot.com").blob(f"pfps/{title}/{uuid4()}.{extension}")

            blob.upload_from_file(pfp)

            url = blob.generate_signed_url(32503680000)

        memories = db.reference("memories")

        memories.push({
            "pfp": url if url else "https://img.freepik.com/free-vector/hand-drawn-magical-dreams-background_23-2149672473.jpg?w=740&t=st=1707043517~exp=1707044117~hmac=df44bdc206d7b245b2886041247a1a015b2602fe971638de5987a5274310a364",
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

            while storage.bucket("kikapees.appspot.com").blob(f"memories/{title}/{filename}").exists():
                suffix += 1
                filename = f'{filename} ({suffix}).{extension}'

            db.reference(f"memories/{uid}/files").push({
                "filename": filename,
                "uploadedOn": datetime.now().timestamp()
            })

            blob = storage.bucket("kikapees.appspot.com").blob(f"memories/{title}/{filename}")

            blob.upload_from_file(file)

        return redirect("/memories")