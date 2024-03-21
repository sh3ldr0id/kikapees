from app.routes.memories import blueprint, reference
from flask import session, render_template, redirect

from app.helpers.validate_token import validate

@blueprint.route("/view/<uid>")
def view(uid):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    memory = reference.child(uid).get()

    if not memory:
        return redirect("/404")
    
    files = []
    
    if "files" in memory:
        for key in memory["files"].keys():
            memory["files"][key]["uid"] = key
            files = memory["files"]

        files = list(memory["files"].values())
        
    return render_template("memories/view.html", uid=uid, memory=memory, files=files)