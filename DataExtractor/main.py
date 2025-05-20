# import os
# import json
# import queue
# import threading
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# from dotenv import load_dotenv
# from scraperScrapy import PDFScraper
# from semanticRetrival import analyze_with_retrieval

# load_dotenv()

# result_queue = queue.Queue()

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

# def main():
#     url_input = input("Inserisci l'URL da cui fare scraping: ").strip()
#     if not url_input.startswith("http"):
#         print("URL non valido.")
#         return

#     os.environ["SITE_TO_SCRAPE"] = url_input

#     output_path = "../output/dataAnalyzed_local.json"
#     os.makedirs("output", exist_ok=True)

#     # Cancella il file se già esiste
#     if os.path.exists(output_path):
#         os.remove(output_path)

#     print("Inizio scraping e analisi...")

#     threading.Thread(target=run_crawler, daemon=True).start()

#     while True:
#         result = result_queue.get()
#         if result == "__FINE__":
#             break
#         print("Risultato ricevuto:")
#         print(json.dumps(result, ensure_ascii=False, indent=2))
#         append_result_to_file(output_path, result)

#     print(f"\nTutti i risultati sono stati salvati progressivamente in {output_path}")

# if __name__ == "__main__":
#     main()
