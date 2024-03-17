from flask import Blueprint
from app.helpers.firebase_apps import FirebaseApps

from firebase_admin import db, storage

blueprint = Blueprint(
    'bucket', 
    __name__
)

firebase_app = FirebaseApps().bucket()

from . import home, create, view, delete