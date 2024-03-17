from flask import Blueprint
from app.helpers.firebase_apps import FirebaseApps


blueprint = Blueprint(
    'memories', 
    __name__
)

firebase_app, nodes = FirebaseApps().memories()

from firebase_admin import storage

bucket = storage.bucket(app=firebase_app)

from . import home, create, view, delete, upload, view_file, delete_file