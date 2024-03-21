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