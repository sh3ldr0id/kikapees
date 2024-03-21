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