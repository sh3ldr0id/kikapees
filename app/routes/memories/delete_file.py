from app.routes.memories import blueprint, firebase_app, nodes
from flask import session, redirect

from firebase_admin import db, storage

from app.helpers.validate_token import validate

@blueprint.route("/view/<uid>/delete/<fileId>")
def delete_file(uid, fileId):
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
    
    file = db.reference(
        app=firebase_app,
        path=f"{uid}/files/{fileId}"
    ).get()

    if not file:
        return redirect("/404")
    
    filename = file["filename"]
    node = file["node"]

    node_app = nodes[node]
    
    bucket = storage.bucket(app=node_app)
    bucket.blob(f"{memory['title']}/files/{filename}").delete()
    bucket.blob(f"{memory['title']}/thumbnails/{filename.split('.')[:-1]}.png").delete()

    db.reference(
        app=firebase_app,
        path=f"{uid}/files"
    ).update({fileId: None})
    
    return redirect(f"/memories/view/{uid}")