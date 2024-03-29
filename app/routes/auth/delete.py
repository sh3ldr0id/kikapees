from app.routes.auth import blueprint
from flask import session, redirect

from firebase_admin import db

from app.helpers.validate_token import validate

@blueprint.route('/delete/<tok>')
def delete(tok):
    token = session.get("token")

    authorized = validate(token)

    if authorized:
        db.reference('auth').update({tok: None})
        db.reference(f'users/{authorized}/sessions').update({tok: None})

    return redirect("/auth/sessions")