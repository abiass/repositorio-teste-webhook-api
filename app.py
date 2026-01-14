from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    if not request.is_json:
        return jsonify(error="Invalid payload"), 400

    data = request.get_json()
    print("Webhook recebido:", data)

    # Tenta reconhecer o formato da WhatsApp Cloud API
    try:
        if data.get("object") == "whatsapp_business_account":
            entries = data.get("entry", [])
            for entry in entries:
                changes = entry.get("changes", [])
                for change in changes:
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    contacts = value.get("contacts", [])
                    for msg in messages:
                        sender = msg.get("from")
                        mtype = msg.get("type")
                        body = None
                        if mtype == "text":
                            body = msg.get("text", {}).get("body")
                        elif mtype == "image":
                            body = "<image>"
                        print(f"Mensagem recebida de {sender}: type={mtype} body={body}")
            return jsonify(status="ok"), 200
    except Exception as e:
        print("Erro ao processar payload:", e)

    # Caso não seja o formato esperado, apenas retorna 200
    return jsonify(status="ignored"), 200


if __name__ == '__main__':
    app.run(port=5000, debug=True)