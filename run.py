from app import create_app
from os.path import exists
from os import mkdir

app = create_app()

if not exists("temp/"):
    mkdir("temp/")

if __name__ == "__main__":
    app.run()