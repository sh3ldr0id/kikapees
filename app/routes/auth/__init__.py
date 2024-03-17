from flask import Blueprint
from ...helpers.firebase_apps import FirebaseApps

from firebase_admin import db

blueprint = Blueprint(
    'auth', 
    __name__
)

firebase_app = FirebaseApps().auth()

from . import login, logout, deactivate, delete, sessions