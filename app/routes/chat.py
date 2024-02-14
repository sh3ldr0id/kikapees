from flask import Blueprint, request, redirect, render_template, session
from firebase_admin import db
from datetime import datetime

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
    
    window = 4
    
    timestamp = int(timestamp)
    previous_timestep = timestamp
    
    new_messages = []

    while len(new_messages) < window:
        messages = db.reference("chats").order_by_child("timestamp").end_at(timestamp).limit_to_last(window).get()
        
        keys = list(messages.keys())
        values = list(messages.values())

        for index, message in enumerate(values):

            if message["timestamp"] >= timestamp:
                break

            if message["deleted"]:
                continue

            key = keys[index]

            if message["by"] != authorized and not message["read"]:
                db.reference(f"chats/{key}").update({
                    "read": True
                })

            new_messages.append(message)

            new_messages[-1]["uid"] = key

        previous_timestep = timestamp
        timestamp = values[0]["timestamp"]

        if previous_timestep == timestamp:
            break

    new_messages = sorted(new_messages, key=lambda x: x['timestamp'])[-window:]

    for message in new_messages:
        print(datetime.fromtimestamp(message["timestamp"]), message["content"])

    print("\n nNEWWW \n")

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

    key = db.reference("chats").push({
        "content": content,
        "by": by,
        "timestamp": timestamp,
        "read": False,
        "deleted": False
    }).key

    new.append(request.json)

    new[-1]["uid"] = key

    return {"uid": key}

deleted = []

@blueprint.route('/delete', methods=["POST"])
def delete_message():
    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
        
    uid = request.json["uid"]

    reference = db.reference(f"chats/{uid}")

    message = reference.get()

    if not message or message['by'] != authorized:
        return {"status": "failed"}

    reference.update({
        "deleted": True
    })

    deleted.append({
        "uid": uid,
        "by": message["by"]
    })

    return {"status": "success"}

@blueprint.route('/polling')
def polling():
    global prev_len

    token = session.get("token")

    authorized = db.reference(f"auth/{token}").get()

    if not authorized:
        return redirect("/")
    
    for index, message in enumerate(deleted):
        if message["by"] != authorized:
            deleted.pop(index)

            return {
                "action": "delete",
                "uid": message["uid"] 
            }

    for index, message in enumerate(new):
        if message["by"] != authorized:
            new.pop(index)

            db.reference(f"chats/{message['uid']}").update({
                "read": True
            })

            return {
                "action": "new",
                "message": message
            }

    return {}