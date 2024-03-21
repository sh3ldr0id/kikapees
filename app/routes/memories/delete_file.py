from app.routes.memories import blueprint, reference, bucket, nodes
from flask import session, redirect

from firebase_admin import storage

from app.helpers.validate_token import validate

@blueprint.route("/view/<uid>/delete/<fileId>")
def delete_file(uid, fileId):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    memory = reference.child(uid).get()

    if not memory:
        return redirect("/404")
    
    file = reference.child(f"{uid}/files/{fileId}").get()

    if not file:
        return redirect("/404")
    
    filename = file["filename"]
    thumbnail_filename = file["thumbnail_filename"]
    node = file["node"]

    node_app = nodes[node]
    
    bucket = storage.bucket(app=node_app)
    bucket.blob(f"memories/{memory['title']}/files/{filename}").delete()
    bucket.blob(f"memories/{memory['title']}/thumbnails/{thumbnail_filename}").delete()

    reference.child(f"{uid}/files").update({fileId: None})
    
    return redirect(f"/memories/view/{uid}")