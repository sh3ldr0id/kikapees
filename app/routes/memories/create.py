from app.routes.memories import blueprint, reference, bucket
from flask import session, render_template, redirect, request

from app.helpers.validate_token import validate

from uuid import uuid4

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

        if reference.order_by_child("title").equal_to(title).get():
            return "A memory with the same name already exists! Please Coose a different name."
        
        thumbnail_filename = f"{uuid4()}."

        if thumbnail:
            thumbnail_filename += thumbnail.filename.rsplit('.', 1)[1]
            
            blob = bucket.blob(thumbnail_filename)
            blob.upload_from_file(thumbnail)
            blob.make_public()

            url = blob.public_url

        else:
            thumbnail_filename += ".png"
                        
            blob = bucket.blob(thumbnail_filename)
            blob.upload_from_file("thumbnails/memory.png")
            blob.make_public()

            url = blob.public_url

        reference.push({
            "title": title,
            "description": description,
            "thumbnail": url,
            "thumbnail_filename": thumbnail_filename,
            "date": date
        })

        return redirect("/memories")