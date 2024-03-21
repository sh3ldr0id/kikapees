from flask import Blueprint
from firebase_admin import db, storage

blueprint = None
reference = None
bucket = None
nodes = None

class Memories:
    def __init__(self, fb_app):
        global blueprint, reference, bucket, nodes

        self.blueprint = Blueprint(
            'memories', 
            __name__
        )

        blueprint = self.blueprint

        firebase_app, nodes = fb_app.memories()

        reference = db.reference(app=firebase_app)
        bucket = storage.bucket(app=firebase_app)

        from . import home, create, view, delete, upload, view_file, delete_file