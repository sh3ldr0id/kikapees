from app.routes.bucket import blueprint, db, storage
from flask import session, render_template, redirect, request

from app.helpers.generate_thumbnail import generate_thumbnail
from app.helpers.validate_token import validate

from uuid import uuid4 
from requests import get
from datetime import datetime

@blueprint.route('/create', methods=["GET", "POST"])
def create():
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        return render_template("bucket/create.html")
    
    elif request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        link = request.form["reel"]
        file = request.files.get("file")

        bucket = db.reference("/")

        if link:
            filename = f"temp/{str(uuid4())}.mp4"

            with open(filename, 'wb') as file:
                file.write(
                    get(
                        get(
                            f"https://instagram-videos.vercel.app/api/video?url={link}"
                        ).json()["data"]["videoUrl"]
                    ).content
                )

            thumbnail_path, content_path = generate_thumbnail(filename)

            storage_bucket = storage.bucket()

            blob = storage_bucket.blob(f"thumbnails")
            blob.upload_from_filename(thumbnail_path)
            blob.make_public()
            thumbnail_url = blob.public_url

            blob = storage_bucket.blob(f"files")
            blob.upload_from_filename(content_path)
            blob.make_public()
            content_url = blob.public_url

        bucket.push({
            "title": title,
            "description": description,
            "thumbnail": thumbnail_url,
            "content": content_url,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "by": authorized
        })

        return redirect("/bucket")