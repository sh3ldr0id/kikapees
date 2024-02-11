from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime
from app import socketio
from flask_socketio import emit

blueprint = Blueprint(
    'chat', 
    __name__
)

def other(user):
    if user == "kunji":
        other = "kunja"

    else:
        other = "kunji"

    return other

@blueprint.route('/')
def home():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    return render_template("chat/home.html", token=token, user=authorized, other=other(authorized))

@socketio.on('connect')
def connected():
    print('Connecteddd')

@socketio.on('new')
def new(data):
    token = data["token"]

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    content = data["content"]
    by = data["by"]
    timestamp = data["timestamp"]

    db.reference("chats/all").push({
        "content": content,
        "by": by,
        "timestamp": timestamp,
        "read": False,
        "deleted": False
    })

    emit("new", data, broadcast=True)