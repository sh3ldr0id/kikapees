from flask import Blueprint

blueprint = None
firebase_app = None
nodes = None

class Bucket:
    def __init__(self, fb_app):
        global blueprint, firebase_app, nodes

        self.blueprint = Blueprint(
            'bucket', 
            __name__
        )

        blueprint = self.blueprint

        firebase_app, nodes = fb_app.bucket()

        from . import home, create, view, delete