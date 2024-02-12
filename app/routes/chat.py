from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime
from time import sleep

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

@blueprint.route('/get/<timestamp>')
def get_messages(timestamp):
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    messages = db.reference("chats").order_by_child("timestamp").end_at(int(timestamp)).limit_to_last(10).get()

    messages = list(messages.values()) if messages else []
    
    new_messages = []

    for message in messages:
        if message["timestamp"] >= int(timestamp):
            break

        new_messages.append(message)

    return {"messages": new_messages} if new_messages else {}

new = []
prev_len = len(new)

@blueprint.route('/message', methods=["POST"])
def new_message():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
        
    content = request.json["content"]
    by = request.json["by"]
    timestamp = request.json["timestamp"]

    db.reference("chats").push({
        "content": content,
        "by": by,
        "timestamp": timestamp,
        "read": False,
        "deleted": False
    })

    new.append(request.json)

    return {}

@blueprint.route('/polling')
def polling():
    global prev_len

    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")

    found = False

    while not found:
        for index, message in enumerate(new):
            if message["by"] != authorized:
                new.pop(index)

                return message

        sleep(0.25)