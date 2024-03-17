from app.routes.memories import blueprint, firebase_app, nodes
from flask import session, render_template, request, redirect

from firebase_admin import db, storage

from app.helpers.generate_thumbnail import generate_thumbnail
from app.helpers.validate_token import validate
from app.helpers.memories_nodes import calculate_space

from datetime import datetime
from os import stat

@blueprint.route('/upload/<uid>', methods=["GET", "POST"])
def upload(uid):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    memory = db.reference(
        app=firebase_app,
        path=uid
    ).get()

    if not memory:
        return redirect("/404")
    
    memory["uid"] = uid

    if request.method == "GET":
        return render_template("memories/upload.html", memory=memory)
    
    elif request.method == "POST":
        files = request.files.getlist("files")

        for file in files:
            thumbnail_path, content_path = generate_thumbnail(file)

            for node, node_app in nodes.items():
                remaining = (10*1024*1024*1024) - calculate_space(node_app)

                file_size = stat(thumbnail_path).st_size / (1024*1024)
                file_size += stat(content_path).st_size / (1024*1024)

                if file_size < remaining:
                    break

            bucket = storage.bucket(app=node_app)

            suffix = 1

            filename = file.filename
            extension = filename.rsplit('.', 1)[1]

            while bucket.blob(f"memories/{memory['title']}/files/{filename}").exists():
                suffix += 1
                filename = f'{filename} ({suffix}).{extension}'

            blob = bucket.blob(f"{memory['title']}/thumbnails/{''.join(filename.split('.')[:-1])}.png")
            blob.upload_from_filename(thumbnail_path)
            blob.make_public()
            thumbnail_url = blob.public_url

            blob = bucket.blob(f"{memory['title']}/files/{filename}")
            blob.upload_from_filename(content_path)
            blob.make_public()
            content_url = blob.public_url

            db.reference(
                app=firebase_app, 
                path=f"{uid}/files"
            ).push({
                "thumbnail": thumbnail_url,
                "content": content_url,
                "filename": filename,
                "node": node,
                "uploadedOn": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        return redirect(f"/memories/view/{uid}")