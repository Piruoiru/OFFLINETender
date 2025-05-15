import os
import json
from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv
from DataExtractor.scraperScrapy import PDFScraper
from DataExtractor.adderLLMInformation import add_information_to_json
from DataExtractor.adderEmbeddingFields import generate_embeddings_for_all_fields

load_dotenv()

analyzer = Flask(__name__)

@analyzer.route("/analyze", methods=["POST"])
def process_site():
    """
    Endpoint per processare un sito web:
    1. Scraping del sito.
    2. Arricchimento dei dati con informazioni LLM.
    3. Generazione di embedding per i campi.
    """
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request"}), 400

    url_to_scrape = data["url"]
    os.environ["SITE_TO_SCRAPE"] = url_to_scrape


    try:
        # Step 1: Scraping del sito
        os.makedirs("output", exist_ok=True)

        output_file_scrapy = "output/dataScrapy.json"
        process = CrawlerProcess(get_project_settings())
        process.crawl(PDFScraper)
        process.start()


        if not os.path.exists(output_file_scrapy):
            return jsonify({"error": "Scraping failed, no data extracted"}), 500

        # Step 2: Arricchimento dei dati con LLM
        output_file_llm = "output/dataAddedInformation.json"
        add_information_to_json(output_file_scrapy, output_file_llm)

        # Step 3: Generazione di embedding per i campi
        output_file_embeddings = "output/dataFinal.json"
        generate_embeddings_for_all_fields(output_file_llm, output_file_embeddings)

        # Step 4: Restituzione del file JSON finale
        with open(output_file_embeddings, "r", encoding="utf-8") as file:
            final_data = json.load(file)
        return jsonify(final_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    analyzer.run(host="0.0.0.0", port=5000)
