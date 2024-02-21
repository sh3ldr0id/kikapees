from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db, storage
from datetime import datetime
from requests import get
from uuid import uuid4
from cv2 import VideoCapture, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, imwrite

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
        reel = request.form["reel"]

        by = authorized["user"]

        filename = None

        if reel:
            try:
                link = get(
                    f"https://instagram-videos.vercel.app/api/video?url={reel}"
                ).json()["data"]["videoUrl"]

                filename = f"temp/{str(uuid4())}.mp4"

                with open(filename, 'wb') as file:
                    file.write(
                        get(link).content
                    )
            
            except:
                return "Invalid Reel Link"
            
        url = None,
        thumbnail = None

        if filename:
            bucket = storage.bucket("kikapees.appspot.com")

            blob = bucket.blob(f"bucket/files")
            blob.upload_from_filename(filename)
            blob.make_public()

            url = blob.public_url

            cap = VideoCapture(filename)

            skip_frames = round(
                int(
                    cap.get(CAP_PROP_FRAME_COUNT)
                ) / 2
            )

            cap.set(CAP_PROP_POS_FRAMES, skip_frames)

            _, frame = cap.read()

            imwrite(f"{filename.split('.')[0]}.png", frame)

            cap.release()

            blob = bucket.blob(f"bucket/thumbnails")
            blob.upload_from_filename(f"{filename.split('.')[0]}.png")
            blob.make_public()

            thumbnail = blob.public_url

        bucket = db.reference("bucket")

        bucket.push({
            "title": title,
            "description": description,
            "url": url,
            "thumbnail": thumbnail,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
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