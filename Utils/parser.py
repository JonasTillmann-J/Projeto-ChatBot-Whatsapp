from flask import jsonify
import datetime

def parse_webhook_message(request):
    """
    Parser robusto para webhook do WhatsApp.
    Retorna um dicionário com dados essenciais da mensagem e um status.
    """
    try:
        data = request.get_json(silent=True) or {}
        mensagem = None  # inicializa
        numero_remetente = None
        nome_perfil_remetente = None
        data_hora_envio = None

        entry = data.get("entry", [])
        if entry:
            entry_item = entry[0]
            changes = entry_item.get("changes", [])
            if changes:
                changes_item = changes[0]
                value = changes_item.get("value", {})
                if value:
                    # Contato
                    contacts = value.get("contacts", [])
                    contact = contacts[0] if contacts else {}
                    profile = contact.get("profile", {})
                    nome_perfil_remetente = profile.get("name")
                    wa_id = contact.get("wa_id")

                    # Mensagem
                    messages = value.get("messages", [])
                    message = messages[0] if messages else {}
                    numero_remetente = message.get("from")
                    mensagem = (message.get("text") or {}).get("body")
                    message_id = message.get("id")
                    raw_timestamp = message.get("timestamp")

                    # Timestamp
                    if raw_timestamp:
                        try:
                            ts = int(raw_timestamp)
                            data_hora_envio = datetime.datetime.fromtimestamp(ts)
                        except Exception:
                            data_hora_envio = None

                    # Metadata adicional
                    metadata = value.get("metadata", {})
                    phone_number_id = metadata.get("phone_number_id")
                    display_phone_number = metadata.get("display_phone_number")
                else:
                    print("⚠️ Payload recebido sem 'value'")
            else:
                print("⚠️ Payload recebido sem 'changes'")
        else:
            print("⚠️ Payload recebido sem 'entry'")

        if mensagem:
            print(f"-------------------------\n{numero_remetente} - {nome_perfil_remetente}\nenviou: {mensagem}\n{data_hora_envio}\n-------------------------")
            status = "mensagem processada com êxito"
            return {
                "message_id": message_id,
                "wa_id": wa_id,
                "from": numero_remetente,
                "name": nome_perfil_remetente,
                "text": mensagem,
                "timestamp": raw_timestamp,
                "sent_at": data_hora_envio,
                "phone_number_id": phone_number_id,
                "display_phone_number": display_phone_number
            }, status
        else:
            print("⚠️ Nenhuma mensagem encontrada no payload")
            return None, "sem mensagem"

    except Exception as e:
        print(f"❌ Ocorreu um erro de execução: {e}")
        return None, "erro de processamento"