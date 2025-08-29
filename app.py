from flask import Flask, app, jsonify, request
from Utils.parser import parse_webhook_message

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        mensagem, status = parse_webhook_message(request)
    except Exception as e:
        print(f"Ouve algum erro de execução em : app.py : parse_webhook_message{e}")

if __name__ == "__main__": app.run(port=5000, debug=True)   