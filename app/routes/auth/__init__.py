from flask import Blueprint

blueprint = None

class Auth:
    def __init__(self):
        global blueprint

        self.blueprint = Blueprint(
            'auth', 
            __name__
        )

        blueprint = self.blueprint

        from . import login, logout, deactivate, delete, sessions