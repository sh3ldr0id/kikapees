from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db, storage
from datetime import datetime
from uuid import uuid4
from moviepy.video.io.VideoFileClip import VideoFileClip
from os.path import exists

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
    
    data = db.reference("memories").order_by_child("date").get()
    
    keys = []

    if data:
        keys = data.keys()

    memories = []

    for key in keys:
        memories.append(
            data[key]
        )

        memories[-1]["uid"] = key

    memories.reverse()
    
    return render_template("memories/home.html", keys=keys, memories=memories)
    
@blueprint.route('/create', methods=["GET", "POST"])
def create():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        return render_template("memories/create.html")
    
    elif request.method == "POST":
        thumbnail = request.files.get("thumbnail")
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        url = "https://img.freepik.com/free-vector/hand-drawn-magical-dreams-background_23-2149672473.jpg?w=740&t=st=1707043517~exp=1707044117~hmac=df44bdc206d7b245b2886041247a1a015b2602fe971638de5987a5274310a364"

        if thumbnail:
            extension = thumbnail.filename.rsplit('.', 1)[1]

            blob = storage.bucket("kikapees.appspot.com").blob(f"memories/{title}/thumbnail.{extension}")

            blob.upload_from_file(thumbnail)

            url = blob.generate_signed_url(32503680000)

        memories = db.reference("memories")

        memories.push({
            "thumbnail": url,
            "title": title,
            "description": description,
            "date": date
        })

        return redirect("/memories")
    
@blueprint.route('/upload/<uid>', methods=["GET", "POST"])
def upload(uid):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    memory = db.reference(f"memories/{uid}").get()

    if not memory:
        return redirect("/404")
    
    memory["uid"] = uid

    if request.method == "GET":
        return render_template("memories/upload.html", memory=memory)
    
    elif request.method == "POST":
        files = request.files.getlist("files")

        for file in files:
            suffix = 1

            filename = file.filename
            extension = filename.rsplit('.', 1)[1]

            while storage.bucket("kikapees.appspot.com").blob(f"memories/{memory['title']}/files/{filename}").exists():
                suffix += 1
                filename = f'{filename} ({suffix}).{extension}'

            blob = storage.bucket("kikapees.appspot.com").blob(f"memories/{memory['title']}/files/{filename}")

            blob.upload_from_file(file)

            blob.make_public()

            url = blob.public_url

            thumbnail = "https://storage.googleapis.com/kikapees.appspot.com/default_thumbnail.svg"

            if extension in ['mp4', 'avi', 'mkv', 'mov']:
                file.save(f"temp/{filename}")

                thumbnail_filename = f"temp/{str(uuid4())}.png"

                print(exists(f"temp/{filename}"))

                clip = VideoFileClip(f"temp/{filename}", audio=False)
                clip.save_frame(0, thumbnail_filename)
                clip.close()

                blob = storage.bucket("kikapees.appspot.com").blob(f"memories/{memory['title']}/thumbnails/{thumbnail_filename}")

                blob.upload_from_filename(f"temp/{filename.rsplit('.', 1)[0]}.png")

                blob.make_public()

                thumbnail = blob.public_url

            elif extension in ["png", "jpg", "jpeg", "gif"]:
                thumbnail = url

            db.reference(f"memories/{uid}/files").push({
                "thumbnail": thumbnail,
                "filename": filename,
                "url": url,
                "uploadedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return redirect(f"/memories/view/{uid}")
    
@blueprint.route("/delete/<uid>")
def delete(uid):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    memory = db.reference(f"memories/{uid}").get()

    if not memory:
        return redirect("/404")
    
    files = db.reference(f"memories/{uid}/files").get()

    if files:
        files = files.keys()
        
        for fileId in files:
            file = db.reference(f"memories/{uid}/files/{fileId}").get()
            print(file)

            blob = storage.bucket("kikapees.appspot.com").blob(f"memories/{memory['title']}/{file['filename']}")
            blob.delete()    

            db.reference(f"memories/{uid}/files").update({fileId: None})

    db.reference(f"memories").update({uid: None})

    return redirect("/memories")
    
@blueprint.route("/view/<uid>")
def view(uid):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    memory = db.reference(f"memories/{uid}").get()

    if not memory:
        return redirect("/404")
    
    files = []
    
    if "files" in memory:
        for key in memory["files"].keys():
            memory["files"][key]["uid"] = key
            
            files = memory["files"]
        files = list(memory["files"].values())
        
    return render_template("memories/view.html", uid=uid, memory=memory, files=files)

@blueprint.route("/view/<uid>/delete/<fileId>")
def delete_file(uid, fileId):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    memory = db.reference(f"memories/{uid}").get()

    if not memory:
        return redirect("/404")
    
    file = db.reference(f"memories/{uid}/files/{fileId}").get()

    if not file:
        return redirect("/404")
    
    blob = storage.bucket("kikapees.appspot.com").blob(f"memories/{memory['title']}/files/{file['filename']}")
    blob.delete()

    db.reference(f"memories/{uid}/files").update({fileId: None})
    
    return redirect(f"/memories/view/{uid}")

@blueprint.route("/view/<uid>/open/<fileId>")
def open(uid, fileId):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    memory = db.reference(f"memories/{uid}").get()

    if not memory:
        return redirect("/404")
    
    file = db.reference(f"memories/{uid}/files/{fileId}").get()

    if not file:
        return redirect("/404")
    
    return f"<img src='{file['url']}'>"