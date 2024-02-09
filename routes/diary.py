from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime

blueprint = Blueprint(
    'diary', 
    __name__
)

def other(user):
    if user == "kunji":
        other = "kunja"

    else:
        other = "kunji"

    return other

@blueprint.route('/')
def home():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    return render_template("diary/home.html", date=datetime.now().strftime('%Y-%m-%d'), other=other(authorized))    

@blueprint.route('/view/<custom_date:date>/<user>')
def view(date, user):
    if not date:
        return redirect("/404")

    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    page = db.reference(f"diary/{date}/{user}").get()
        
    return render_template("diary/page.html", date=date.strftime('%A, %d %B %Y'), user=authorized.capitalize(), page=page)
    
@blueprint.route('/write/<custom_date:date>', methods=["GET", "POST"])
def write(date):
    if not date:
        print(date)
        return redirect("/404")

    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    user = authorized["user"]

    if request.method == "GET":
        page = db.reference(f"diary/{date}/{user}").get()

        return render_template("diary/write.html", date=date.strftime('%A, %d %B %Y'), other=other(authorized).capitalize(), page=page)
    
    elif request.method == "POST":
        content = request.form["content"]
    
        page = db.reference(f"diary/{date}").update({
            user: content
        })

        return redirect(f"/diary/view/{date}/{user}")