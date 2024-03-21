from flask import Blueprint

blueprint = None
firebase_app = None
nodes = None

class Chat:
    def __init__(self, fb_app):
        global blueprint, firebase_app, nodes

        self.blueprint = Blueprint(
            'chat', 
            __name__
        )

        blueprint = self.blueprint

        firebase_app, nodes = fb_app.chat()

        from . import home, create, view, delete