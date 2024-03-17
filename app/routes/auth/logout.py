from app.routes.auth import blueprint
from flask import session, redirect

from firebase_admin import db

@blueprint.route('/logout')
def logout():
    token = session.get("token")

    authorized = db.reference(f'auth/{token}').get()

    if authorized:
        db.reference('auth').update({
            token: None
        })

    db.reference(f'users/{authorized}/sessions/{token}').update({"active": False})

    session["token"] = None

    return redirect("/")