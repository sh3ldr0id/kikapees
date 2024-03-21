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