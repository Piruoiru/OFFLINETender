from flask import Flask, request, Response, stream_with_context
from dotenv import load_dotenv
import os, json
from controller import generate_analysis_stream
from utils.storage import reset_output_file
import os

load_dotenv()
analyzer = Flask(__name__)
output_path = "output/dataAnalyzed.json"

@analyzer.route("/analyze", methods=["POST"])
def stream_analysis():
    """
    Descrizione: 
        Endpoint Flask per avviare l'analisi e restituire i risultati in streaming.
    
    Input:
        Richiesta HTTP contenente un JSON con il campo url.
    
    Output:
        Stream di risultati JSON.
    
    Comportamento:
        Legge l'URL dalla richiesta.
        Resetta il file di output.
        Avvia il crawler e restituisce i risultati in streaming.
    """
    data = request.get_json()
    if not data or "url" not in data:
        return Response(json.dumps({"error": "Fornire 'url': 'https://...'"}, ensure_ascii=False), status=400)

    os.environ["SITE_TO_SCRAPE"] = data["url"]
    reset_output_file(output_path)
    print("[DEBUG] Flask usa MODEL_LLM_API =", os.getenv("MODEL_LLM_API"))

    return Response(
        stream_with_context(generate_analysis_stream(output_path)),
        mimetype='application/json'
    )

if __name__ == "__main__":
    analyzer.run(host="0.0.0.0", port=5000)
