import os
import json
import subprocess
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from DataExtractor.adderLLMInformation import add_information_to_json
from DataExtractor.adderEmbeddingFields import generate_embeddings_for_all_fields

load_dotenv()

app = Flask(__name__)

@app.route("/analyze", methods=["POST"])
def process_site():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400

    url_to_scrape = data["url"]
    os.environ["SITE_TO_SCRAPE"] = url_to_scrape

    try:
        os.makedirs("output", exist_ok=True)

        # Chiamata allo scraper come processo separato
        result = subprocess.run(
            ["python", "runScraper.py"], 
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return jsonify({
                "error": "Scraper failed",
                "details": result.stderr
            }), 500

        output_file_scrapy = "output/dataScrapy.json"
        if not os.path.exists(output_file_scrapy):
            return jsonify({"error": "Scraping failed, no data extracted"}), 500

        # Step 2: Arricchimento dati LLM
        print("Arricchimento dei dati con LLM...")
        output_file_llm = "output/dataAddedInformation.json"
        add_information_to_json(output_file_scrapy, output_file_llm)
        print("Arricchimento completato.")

        # Step 3: Generazione embedding
        print("Generazione di embedding per i campi...")
        output_file_embeddings = "output/dataFinal.json"
        generate_embeddings_for_all_fields(output_file_llm, output_file_embeddings)
        print("Generazione di embedding completata.")

        with open(output_file_embeddings, "r", encoding="utf-8") as file:
            final_data = json.load(file)

        return jsonify(final_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
