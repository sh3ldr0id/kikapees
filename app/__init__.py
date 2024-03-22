from flask import Flask, session, redirect, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from app.helpers.validate_token import validate
from app.helpers.custom_date_converter import CustomDateConverter
from app.helpers.firebase_apps import FirebaseApps

from firebase_admin import storage

def create_app(host="127.0.0.1", port=5000):
    app = Flask(__name__)
    app.secret_key = 'SECRET_KEY'

    app.url_map.converters['custom_date'] = CustomDateConverter

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    @app.errorhandler(404)
    def not_found(e):
        return "Invalid/Broken URL"

    @app.errorhandler(500)
    def not_found(e):
        return "Sorryyyy!!! I messed up somewhere..."

    @app.route("/")
    def index():
        token = session.get("token")

        authorized = validate(token)

        if authorized:
            return render_template("index.html")
        
        else:
            return redirect("/auth/login")
        
    from app.routes.auth import Auth
    from app.routes.memories import Memories
    from app.routes.bucket import Bucket
    # from app.routes.chat import Chat

    firebase_app = FirebaseApps()

    firebase_app.auth()

    blobs = storage.bucket().list_blobs(prefix="credentials")

    for blob in blobs:
        if blob.name.endswith("/"):
            continue

        if "dffs" in blob.name:
            blob.download_to_filename(f"Firebase Credentials/DFFS/{blob.name.split('/')[-1]}")
        
        else:
            blob.download_to_filename(f"Firebase Credentials/{blob.name.split('/')[-1]}")

    firebase_app.load_nodes()

    auth_blueprint = Auth().blueprint
    bucket_blueprint = Bucket(firebase_app).blueprint
    memories_blueprint = Memories(firebase_app).blueprint
    # chat_blueprint = Chat(firebase_app).blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(bucket_blueprint, url_prefix='/bucket')
    app.register_blueprint(memories_blueprint, url_prefix='/memories')
    # app.register_blueprint(chat_blueprint, url_prefix='/chat')

    return app