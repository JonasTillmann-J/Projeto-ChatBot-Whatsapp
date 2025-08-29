from flask import Flask, app, jsonify, request
from Utils.parser import parse_webhook_message

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])

def webhook():

    mensagem, status = parse_webhook_message(request)

    if mensagem.get("status") == 'mensagem processada':
        return jsonify(mensagem), status
    else:
        return jsonify(mensagem), status

if __name__ == "__main__": app.run(port=5000, debug=True)