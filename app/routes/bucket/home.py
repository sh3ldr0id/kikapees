from app.routes.bucket import blueprint, firebase_app
from flask import session, render_template, redirect

from firebase_admin import db

from app.helpers.validate_token import validate

@blueprint.route('/')
def home():
    token = session.get("token")

    authorized = validate(token)

    if not authorized:
        return redirect("/")
    
    data = db.reference(app=firebase_app).get()

    bucket = []

    if data:
        for key in data.keys():
            bucket.append(data[key])
            bucket[-1]["uid"] = key

    return render_template("bucket/home.html", bucket=bucket)