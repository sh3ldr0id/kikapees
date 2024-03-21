from app import create_app
from os.path import exists
from os import mkdir

if not exists("temp/"):
    mkdir("temp/")

if not exists("Firebase Credentials/"):
    mkdir("Firebase Credentials/")
    mkdir("Firebase Credentials/DFFS/")

elif not exists("Firebase Credentials/DFFS"):
    mkdir("Firebase Credentials/DFFS/")

app = create_app()

if __name__ == "__main__":
    app.run()