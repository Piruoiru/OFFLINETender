# import os
# import json
# import queue
# import threading
# from flask import Flask, request, Response, stream_with_context
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from dotenv import load_dotenv
# from DataExtractor.scraperScrapy import PDFScraper
# from DataExtractor.semanticRetrival import analyze_with_retrieval

# load_dotenv()
# analyzer = Flask(__name__)

# result_queue = queue.Queue()
# output_path = "output/dataAnalyzed.json"

# def append_result_to_file(path, nuovo_risultato):
#     """Aggiunge un nuovo risultato a un file JSON come lista di oggetti."""
#     if os.path.exists(path):
#         with open(path, "r", encoding="utf-8") as f:
#             try:
#                 dati = json.load(f)
#                 if not isinstance(dati, list):
#                     dati = []
#             except json.JSONDecodeError:
#                 dati = []
#     else:
#         dati = []

#     dati.append(nuovo_risultato)

#     with open(path, "w", encoding="utf-8") as f:
#         json.dump(dati, f, ensure_ascii=False, indent=4)

# class StreamingPDFScraper(PDFScraper):
#     def handle_file(self, response):
#         """Processa ogni PDF, analizza e mette in coda il risultato."""
#         title = response.meta['title']
#         url = response.url
#         content_type = response.headers.get('Content-Type', b'').decode('utf-8')

#         if "application/pdf" in content_type:
#             content = self.process_pdf(response)
#         else:
#             content = f"File di tipo {content_type} scaricato."

#         try:
#             if not content.strip():
#                 raise ValueError("Contenuto PDF vuoto.")
#             risposta = analyze_with_retrieval(content)
#             risultato = {
#                 "Titolo": title,
#                 "URL": url,
#                 "Risposta": risposta
#             }
#         except Exception as e:
#             risultato = {
#                 "Titolo": title,
#                 "URL": url,
#                 "Errore": str(e)
#             }

#         result_queue.put(risultato)

# def run_crawler():
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(StreamingPDFScraper)
#     process.start()
#     result_queue.put("__FINE__")

# @analyzer.route("/analyze", methods=["POST"])
# def stream_analysis():
#     data = request.get_json()
#     if not data or "url" not in data:
#         return Response(json.dumps({"error": "Fornire 'url': 'https://...'"}, ensure_ascii=False), status=400)

#     url_to_scrape = data["url"]
#     os.environ["SITE_TO_SCRAPE"] = url_to_scrape

#     # reset output
#     os.makedirs("output", exist_ok=True)
#     if os.path.exists(output_path):
#         os.remove(output_path)

#     def generate_stream():
#         threading.Thread(target=run_crawler, daemon=True).start()
#         while True:
#             result = result_queue.get()
#             if result == "__FINE__":
#                 break
#             append_result_to_file(output_path, result)
#             yield json.dumps(result, ensure_ascii=False) + "\n"

#     return Response(stream_with_context(generate_stream()), mimetype='application/json')

# if __name__ == "__main__":
#     analyzer.run(host="0.0.0.0", port=5000)

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
