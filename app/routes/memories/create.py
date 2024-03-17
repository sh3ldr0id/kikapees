from app.routes.memories import blueprint, firebase_app, bucket
from flask import session, render_template, redirect, request

from firebase_admin import db

from app.helpers.validate_token import validate

@blueprint.route('/create', methods=["GET", "POST"])
def create():
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")

    if request.method == "GET":
        return render_template("memories/create.html")
    
    elif request.method == "POST":
        thumbnail = request.files.get("thumbnail")
        title = request.form["title"]
        description = request.form["description"]
        date = request.form["date"]

        url = "https://storage.googleapis.com/kikapees.appspot.com/memories/default_memory_thumbnail.svg"

        if thumbnail:
            extension = thumbnail.filename.rsplit('.', 1)[1]
            
            blob = bucket.blob(f"{title}/thumbnail.{extension}")
            blob.upload_from_file(thumbnail)
            blob.make_public()

            url = blob.public_url

        memories = db.reference(app=firebase_app)

        memories.push({
            "thumbnail": url,
            "title": title,
            "description": description,
            "date": date
        })

        return redirect("/memories")