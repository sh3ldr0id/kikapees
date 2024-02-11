from flask import Flask, session, redirect, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from app.database.database import init_db
from firebase_admin import db
from werkzeug.routing import BaseConverter
from datetime import datetime

class CustomDateConverter(BaseConverter):
    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d').date()
        
        except ValueError:
            return None

    def to_url(self, value):
        return value.strftime('%Y-%m-%d')


def create_app(host="127.0.0.1", port=5000):
    app = Flask(__name__)
    app.secret_key = 'SECRET_KEY'

    app.url_map.converters['custom_date'] = CustomDateConverter

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

    init_db()

    @app.errorhandler(404)
    def not_found(e):
        return "Invalid/Broken URL"

    @app.errorhandler(500)
    def not_found(e):
        return "Sorryyyy!!! I fucked up somewhere..."

    @app.route("/")
    def index():
        token = session.get("token")

        authorized = db.reference(f"auth/{token}").get()

        if authorized:
            return render_template("index.html")
        
        else:
            return redirect("/auth/login")

    from .routes.auth import blueprint as auth_blueprint
    from .routes.bucket import blueprint as bucket_blueprint
    from .routes.memories import blueprint as memories_blueprint
    from .routes.diary import blueprint as diary_blueprint
    from .routes.chat import blueprint as chat_blueprint

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(bucket_blueprint, url_prefix='/bucket')
    app.register_blueprint(memories_blueprint, url_prefix='/memories')
    app.register_blueprint(diary_blueprint, url_prefix='/diary')
    app.register_blueprint(chat_blueprint, url_prefix='/chat')

    return app