from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db, storage
from datetime import datetime
from requests import get
from uuid import uuid4
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, imwrite
from os import remove

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

        link = request.form["reel"]
        file = request.files["file"]

        bucket = db.reference("bucket")

        if link:
            try:
                filename = f"temp/{str(uuid4())}"

                if "https://www.instagram.com/" in link:
                    with open(f"{filename}.mp4", 'wb') as file:
                        file.write(
                            get(
                                get(
                                    f"https://instagram-videos.vercel.app/api/video?url={link}"
                                ).json()["data"]["videoUrl"]
                            ).content
                        )

                storage_bucket = storage.bucket("kikapees.appspot.com")

                blob = storage_bucket.blob(f"bucket/files")
                blob.upload_from_filename(f"{filename}.mp4")
                blob.make_public()
                url = blob.public_url

                cap = VideoCapture(filename)
                skip_frames = round(int(cap.get(CAP_PROP_FRAME_COUNT)) / 2)
                cap.set(CAP_PROP_POS_FRAMES, skip_frames)
                _, frame = cap.read()
                imwrite(f"{filename}.png", frame)
                cap.release()

                blob = storage_bucket.blob(f"bucket/thumbnails")
                blob.upload_from_filename(f"{filename}.png")
                blob.make_public()
                thumbnail = blob.public_url

                remove(f"{filename}.mp4")
                remove(f"{filename}.png")
            
            except:
                return "Invalid Reel Link"

        bucket.push({
            "title": title,
            "description": description,
            "type": "text",
            "thumbnail": thumbnail,
            "url": url,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "by": authorized
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