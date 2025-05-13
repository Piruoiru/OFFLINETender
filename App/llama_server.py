from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/api/completions', methods=['POST'])
def llama_completions():
    """
    Endpoint per simulare il completamento di testo con Llama.
    """
    try:
        # Ottieni i dati dalla richiesta
        data = request.get_json()

        # Simula una risposta dal modello Llama
        prompt = data.get("prompt", "")
        model = data.get("model", "llama3.1")

        # Genera una risposta simulata
        response = {
            "completion": json.dumps({
                "Provider": "Esempio Provider",
                "Data di pubblicazione": "2025-05-13",
                "Data di termine di consegna": "2025-06-01",
                "Tipologia di procedura": "Esempio Procedura",
                "Finalità": "Esempio Finalità",
                # Aggiungi altri campi simulati qui
            })
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11435)