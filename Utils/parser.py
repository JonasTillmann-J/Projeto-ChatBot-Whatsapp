from flask import jsonify

def parse_webhook_message(request):

    data = request.get_json()
    print("Mensagem recebida:", data)

    if "entry" in data:
        changes = data["entry"][0].get("changes", [])

        if changes:
            messages = changes[0]["value"].get("messages", [])

            if messages:
                msg_text = messages[0]["text"]["body"]
                sender = messages[0]["from"]
                print(f"-------------------------\nMensagem de {sender}\n\n{msg_text}\n-------------------------")
                return {"status": "mensagem processada"}, 200

    return {"status": "ignorado"}, 200
