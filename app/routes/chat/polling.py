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