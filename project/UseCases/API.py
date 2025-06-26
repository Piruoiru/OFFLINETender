from flask import Flask, request, jsonify
from QueryProcessor import QueryProcessor
import traceback
import threading
import Main

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        message = data.get('message')
        conversation_id = data.get('conversation_id')

        if not message or not conversation_id:
            return jsonify({'error': 'Invalid input'}), 400

        qp = QueryProcessor(conversation_id)
        result = qp.run(message)

        # Se `result` è già un dict con chiave 'error', lo ritorniamo come tale
        if isinstance(result, dict) and 'error' in result:
            return jsonify(result), 500

        return jsonify({
            'response': result,
            'conversation_id': qp.conversation_id
        })

    except Exception as e:
        return jsonify({
            'error': 'Errore lato server',
            'exception': str(e),
            'trace': traceback.format_exc()
        }), 500
    
@app.route('/analyze', methods=['POST'])
def analyze():
    """Avvia l'analisi completa definita in Main.run() in background.

    Restituisce 202 Accepted immediatamente in modo che l'API rimanga reattiva.
    """
    try:
        # Lancia Main.run() in un thread separato per non bloccare la richiesta
        thread = threading.Thread(target=Main.run, daemon=True, name="Analyzer")
        thread.start()

        # 202 Accepted: il processo è stato avviato
        return jsonify({'status': 'Analisi avviata'}), 202

    except Exception as e:
        return jsonify({
            'error': 'Errore lato server',
            'exception': str(e),
            'trace': traceback.format_exc()
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
