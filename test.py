from firebase_admin import credentials, initialize_app, db, storage

cred = credentials.Certificate("config/creds.json")

initialize_app(cred, {
    'databaseURL': 'https://kikapees-default-rtdb.asia-southeast1.firebasedatabase.app'
})

bucket = storage.bucket("kikapees.appspot.com")

blob = bucket.blob("memories/default_memory_thumbnail.svg")

blob.make_private()

print(blob.public_url)