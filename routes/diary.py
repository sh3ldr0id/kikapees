from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime

blueprint = Blueprint(
    'diary', 
    __name__
)

@blueprint.route('/view/<date>/<user>')
def view(date, user):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    page = db.reference(f"diary/{date}/{user}").get()

    return render_template("diary/page.html", date=date, page=page)
    
@blueprint.route('/write/<date>', methods=["GET", "POST"])
def write(date):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    user = authorized["user"]

    if request.method == "GET":
        page = db.reference(f"diary/{date}/{user}").get()

        return render_template("diary/write.html", page=page)
    
    elif request.method == "POST":
        day = request.form["day"]
        content = request.form["content"]
    
        page = db.reference(f"diary/{date}").update({
            user: {
                "day": day,
                "content": content
            }
        })

        print(date, content)

        return redirect(f"/diary/view/{date}/{user}")