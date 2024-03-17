from app.routes.auth import blueprint
from flask import session, render_template, redirect

from firebase_admin import db

@blueprint.route("/sessions")
def sessions():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    sessions = db.reference(f"users/{authorized}/sessions").order_by_child("time").get()

    if sessions:
        tokens = list(sessions.keys())
        sessions = list(sessions.values())

        for index in range(len(sessions)):
            sessions[index]["active"] = "Active" if sessions[index]["active"] else "Inactive"
            sessions[index]["token"] = tokens[index]

    sessions.reverse()

    return render_template("auth/sessions.html", sessions=sessions)