from flask import Flask, session, redirect
from database.database import init_db
from firebase_admin import db

from routes.auth import blueprint as auth_blueprint
from routes.bucket import blueprint as bucket_blueprint
from routes.memories import blueprint as memories_blueprint

app = Flask(__name__)
app.secret_key = 'SECRET_KEY'

init_db()

@app.route("/404")
def error():
    return "Not Found"

@app.route("/")
def index():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if authorized:
        return redirect("/bucket")
    
    else:
        return redirect("/auth/login")

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(bucket_blueprint, url_prefix='/bucket')
app.register_blueprint(memories_blueprint, url_prefix='/memories')

if __name__ == "__main__":
    app.run()