import firebase_admin
from firebase_admin import credentials

def init_db():
    cred = credentials.Certificate("config/creds.json")

    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://kikapees-default-rtdb.asia-southeast1.firebasedatabase.app'
    })