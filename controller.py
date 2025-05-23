# import os
# import json
# import queue
# import threading
# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings
# import psycopg2
# from DataExtractor.scraperScrapy import PDFScraper
# from DataExtractor.semanticRetrival import retrieve_similar_chunks
# from DataExtractor.embedderLocal import get_embedding
# from DataExtractor.pgvector_utils import insert_chunk

# result_queue = queue.Queue()

# class StreamingPDFScraper(PDFScraper):
#     def handle_file(self, response):
#         """
#         Descrizione: 
#             Processa i PDF scaricati e analizza il contenuto con retrieval semantico.
        
#         Input:
#             response: Oggetto Scrapy contenente il file scaricato.
        
#         Output:
#             Nessuno (aggiunge i risultati a una coda).
        
#         Comportamento: 
#             Estrae il contenuto del PDF, lo analizza con analyze_with_retrieval e mette il risultato in una coda.
#         """
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
#             embedding = get_embedding(content)
#             # risposta = analyze_with_retrieval(content)

#             # Salva nel database
#             # insert_document(title, url, content, embedding)
#             risultato = {
#                 "Titolo": title,
#                 "URL": url,
#                 # "Risposta": risposta
#             }
#         except Exception as e:
#             risultato = {
#                 "Titolo": title,
#                 "URL": url,
#                 "Errore": str(e)
#             }

#         result_queue.put(risultato)

# def run_crawler():
#     """
#     Descrizione: 
#         Avvia il crawler Scrapy.
    
#     Input: 
#         Nessuno.
    
#     Output: 
#         Nessuno.
    
#     Comportamento: 
#         Esegue il crawler e aggiunge un segnale di fine alla coda.
#     """
#     process = CrawlerProcess(get_project_settings())
#     process.crawl(StreamingPDFScraper)
#     process.start(stop_after_crawl=True)
#     result_queue.put("__FINE__")


# def generate_analysis_stream(_unused_output_path):
#     """
#     Genera uno stream di risultati analizzati e li salva direttamente nel DB.
#     """
#     # Connessione al DB una volta sola
#     conn = psycopg2.connect(
#         dbname=os.getenv("POSTGRES_DB"),
#         user=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=os.getenv("POSTGRES_PORT")
#     )
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO Site (SiteToScrape) VALUES (%s) RETURNING IDSite;", (os.getenv("SITE_TO_SCRAPE"),))
#     site_id = cursor.fetchone()[0]
#     cursor.close()

#     threading.Thread(target=run_crawler, daemon=True).start()
#     while True:
#         result = result_queue.get()
#         if result == "__FINE__":
#             break

#         # Salva subito nel database
#         # insert_single_result(conn, result, site_id)

#         # Stream al client
#         yield json.dumps(result, ensure_ascii=False) + "\n"

#     conn.close()
