from firebase_admin.credentials import Certificate
from firebase_admin import initialize_app

from app.helpers.memories_nodes import get_available, load_app

class FirebaseApps:
    def auth(self):
        cred = Certificate("Firebase Credentials/creds.json")

        app = initialize_app(cred, {
            'databaseURL': 'https://kikapees-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

        return app
    
    def bucket(self):
        cred = Certificate("Firebase Credentials/bucket.json")

        app = initialize_app(cred, {
            'databaseURL': 'https://kikapees-bucket-default-rtdb.asia-southeast1.firebasedatabase.app/',
        }, "bucket")

        return app
    
    def memories(self):
        cred = Certificate("Firebase Credentials/memories.json")

        app = initialize_app(cred, {
            'databaseURL': 'https://kikapees-memories-default-rtdb.asia-southeast1.firebasedatabase.app/',
            'storageBucket': 'kikapees-memories.appspot.com'
        }, "memories")

        nodes = {}

        for node in get_available():
            nodes[node] = load_app(node)

        return app, nodes
    
    def chat(self):
        cred = Certificate("Firebase Credentials/chat.json")

        app = initialize_app(cred, {
            'databaseURL': 'https://kikapees-chat-default-rtdb.asia-southeast1.firebasedatabase.app/'
        }, "chat")

        return app