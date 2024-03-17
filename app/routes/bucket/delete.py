from app.routes.bucket import blueprint, db
from flask import session, redirect

from app.helpers.validate_token import validate

@blueprint.route('/delete/<uid>', methods=["GET", "POST"])
def delete(uid):
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    fish = db.reference(f"{uid}")

    if not fish.get():
        return redirect("/404")
    
    fish.set({})

    return redirect("/bucket")