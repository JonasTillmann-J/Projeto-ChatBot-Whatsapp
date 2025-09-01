from flask import Flask, jsonify, request
from Utils.parser import parse_webhook_message

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Chamando a função para pegar a mensagem e o status
        mensagem_data, status = parse_webhook_message(request)
        
        # Verifica se a função retornou valores válidos
        if mensagem_data is None:
            return jsonify({"error": "Mensagem invalida"}), 400

        # Se tudo estiver certo, retorna sucesso com status 200
        return jsonify({"message": "Tudo esta certo", "data": mensagem_data, "status": status}), 200

    except Exception as e:
        # Em caso de erro, imprime a exceção e retorna um erro 500
        print(f"Ocorreu um erro de execucao em app.py : parse_webhook_message: {e}")
        return jsonify({"error": "Erro no servidor"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)