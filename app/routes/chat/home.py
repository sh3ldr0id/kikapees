@blueprint.route('/')
def home():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    return render_template("chat/home.html", token=token, user=authorized, other=other(authorized))