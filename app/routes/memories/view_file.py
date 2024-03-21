from app.routes.memories import blueprint, reference
from flask import session, redirect

from app.helpers.validate_token import validate

@blueprint.route("/view/<uid>/open/<fileId>")
def open(uid, fileId):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    memory = reference.child(uid).get()

    if not memory:
        return redirect("/404")
    
    if uid == fileId:
        return f"<img src='{memory['thumbnail']}'>"
    
    file = reference.child(f"{uid}/files/{fileId}").get()

    if not file:
        return redirect("/404")
    
    if file["filename"].split(".")[-1] in ["png", "jpg", "jpeg", "gif"]:
        return f"<img src='{file['content']}'>"
        
    return redirect(file["content"])