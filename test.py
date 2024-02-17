from firebase_admin import credentials, initialize_app, db, storage

cred = credentials.Certificate("config/creds.json")

initialize_app(cred, {
    'databaseURL': 'https://kikapees-default-rtdb.asia-southeast1.firebasedatabase.app'
})

memories = db.reference("memories/").get().values()

titles = []

for memory in memories:
    titles.append(memory["title"])

bucket = storage.bucket("kikapees.appspot.com")

files = bucket.list_blobs(prefix="pfps")
names = [file.name for file in files]

dicts = {}

for name in names:
    title = name.split("/")[1]

    if title not in dicts.keys():
        dicts[title] = []

    dicts[title].append(name)

for item in dicts.values():
    if len(item) == 1:
        continue

    item = item[:-1]
    
    for filename in item:
        bucket.blob(filename).delete()