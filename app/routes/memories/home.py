from app.routes.memories import blueprint, firebase_app
from flask import session, render_template, redirect

from firebase_admin import db

from app.helpers.validate_token import validate

@blueprint.route('/')
def home():
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    data = db.reference(app=firebase_app).order_by_child("date").get()
    
    keys = []

    if data:
        keys = data.keys()

    memories = []

    for key in keys:
        memories.append(
            data[key]
        )

        memories[-1]["uid"] = key

    memories.reverse()
    
    return render_template("memories/home.html", keys=keys, memories=memories)