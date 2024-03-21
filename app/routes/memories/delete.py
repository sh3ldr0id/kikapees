from app.routes.memories import blueprint, reference, bucket, nodes
from flask import session, redirect

from firebase_admin import storage

from app.helpers.validate_token import validate

@blueprint.route("/delete/<uid>")
def delete(uid):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    memory = reference.child(uid).get()

    if not memory:
        return redirect("/404")
    
    

    reference.update({uid: None})
    bucket.blob(memory["thumbnail_filename"]).delete()

    if not "files" in memory.keys():
        return redirect("/memories")
    
    files = memory["files"]
        
    for file in files.values():
        filename = file['filename']
        thumbnail_filename = file['thumbnail_filename']
        node = file["node"]

        node_app = nodes[node]

        node_bucket = storage.bucket(app=node_app)
        node_bucket.blob(f"memories/{memory['title']}/files/{filename}").delete()
        node_bucket.blob(f"memories/{memory['title']}/thumbnails/{thumbnail_filename}").delete()

    return redirect("/memories")