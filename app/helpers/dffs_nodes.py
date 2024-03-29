from firebase_admin import initialize_app, storage
from firebase_admin.credentials import Certificate

from os import listdir

def load_app(name):
    cred = Certificate(f"Firebase Credentials/DFFS/{name}.json")

    app = initialize_app(
        credential=cred, 
        options={
            "storageBucket": f"kikapees-dffs-{name}.appspot.com"
        },
        name=name
    )

    return app

def get_available():
    files = listdir("Firebase Credentials/DFFS/")

    available = [file.split(".")[0] for file in files]

    return available

def calculate_space(node_app):
    bucket = storage.bucket(app=node_app)

    blobs = bucket.list_blobs()

    total_size = 0

    for blob in blobs:
        total_size += blob.size

    total_size_mb = total_size / (1024 * 1024)

    return total_size_mb