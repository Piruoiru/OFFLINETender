import os
import json
import queue
import threading
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from DataExtractor.scraperScrapy import PDFScraper
from DataExtractor.semanticRetrival import analyze_with_retrieval
from utils.storage import append_result_to_file

result_queue = queue.Queue()

class StreamingPDFScraper(PDFScraper):
    def handle_file(self, response):
        """
        Descrizione: 
            Processa i PDF scaricati e analizza il contenuto con retrieval semantico.
        
        Input:
            response: Oggetto Scrapy contenente il file scaricato.
        
        Output:
            Nessuno (aggiunge i risultati a una coda).
        
        Comportamento: 
            Estrae il contenuto del PDF, lo analizza con analyze_with_retrieval e mette il risultato in una coda.
        """
        title = response.meta['title']
        url = response.url
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')

        if "application/pdf" in content_type:
            content = self.process_pdf(response)
        else:
            content = f"File di tipo {content_type} scaricato."

        try:
            if not content.strip():
                raise ValueError("Contenuto PDF vuoto.")
            risposta = analyze_with_retrieval(content)
            risultato = {
                "Titolo": title,
                "URL": url,
                "Risposta": risposta
            }
        except Exception as e:
            risultato = {
                "Titolo": title,
                "URL": url,
                "Errore": str(e)
            }

        result_queue.put(risultato)

def run_crawler():
    """
    Descrizione: 
        Avvia il crawler Scrapy.
    
    Input: 
        Nessuno.
    
    Output: 
        Nessuno.
    
    Comportamento: 
        Esegue il crawler e aggiunge un segnale di fine alla coda.
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(StreamingPDFScraper)
    process.start(stop_after_crawl=True)
    result_queue.put("__FINE__")

def generate_analysis_stream(output_path):
    """
    Descrizione: 
        Genera uno stream di risultati analizzati.
    
    Input:
        output_path (str): Percorso del file di output.
    
    Output:
        Generatore di stringhe JSON.
    
    Comportamento: 
        Avvia il crawler in un thread separato e restituisce i risultati dalla coda.
    """
    threading.Thread(target=run_crawler, daemon=True).start()
    while True:
        result = result_queue.get()
        if result == "__FINE__":
            break
        append_result_to_file(output_path, result)
        yield json.dumps(result, ensure_ascii=False) + "\n"
