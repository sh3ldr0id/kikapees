from app.routes.bucket import blueprint, firebase_app
from flask import session, render_template, redirect

from firebase_admin import db

from app.helpers.validate_token import validate

@blueprint.route('/view/<uid>', methods=["GET", "POST"])
def view(uid):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    fish = db.reference(
        app=firebase_app,
        path=uid
    ).get()

    if not fish:
        return redirect("/404")
    
    fish["uid"] = uid
    
    return render_template("bucket/view.html", fish=fish)