from app.routes.auth import blueprint, db
from flask import session, redirect

from app.helpers.validate_token import validate

@blueprint.route('/deactivate/<tok>')
def deactivate(tok):
    token = session.get("token")
    authorized = validate(token)
    
    db.reference(f'users/{authorized}/sessions/{tok}').update({"active": False})

    return redirect("/auth/sessions")