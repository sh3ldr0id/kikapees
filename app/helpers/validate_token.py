from firebase_admin import db

def validate(token):
    authorized = db.reference(f"auth/{token}").get()

    return authorized