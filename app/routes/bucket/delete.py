from app.routes.bucket import blueprint, firebase_app
from flask import session, redirect

from firebase_admin import db

from app.helpers.validate_token import validate

@blueprint.route('/delete/<uid>', methods=["GET", "POST"])
def delete(uid):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    fish = db.reference(
        app=firebase_app,
        path=uid
    )

    if not fish.get():
        return redirect("/404")
    
    fish.set({})

    return redirect("/bucket")