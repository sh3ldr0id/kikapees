from app.routes.auth import blueprint, db
from flask import session, render_template, redirect, request

from app.helpers.validate_token import validate
from app.helpers.get_location import get_location
from app.helpers.hash_passsword import hash_password

from datetime import datetime
from uuid import uuid4

@blueprint.route('/login', methods=["GET", "POST"])
def login():
    token = session.get("token")

    authorized = validate(token)

    if authorized:
        return redirect("/")
    
    if request.method == "GET":
        return render_template("auth/login.html")
        
    elif request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        password_hash = db.reference(f"users/{user}/password").get()

        print(password_hash, hash_password(password))

        if hash_password(password) == password_hash:
            token = str(uuid4())

            db.reference('auth').update({token: user})

            location = get_location(request.remote_addr)

            db.reference(f"users/{user}/sessions/{token}").update({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "active": True,
                "ip": request.remote_addr,
                "location": location
            })

            session["token"] = token

            return redirect("/")
        
        else: 
            return "Incorrect Password"