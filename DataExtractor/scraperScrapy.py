import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import json
import PyPDF2
from io import BytesIO
from dotenv import load_dotenv
import os
import requests
from scrapy.http import HtmlResponse


load_dotenv()

class PDFScraper(scrapy.Spider):
    name = "pdf_scraper"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [os.environ["SITE_TO_SCRAPE"]] 

    extracted_data = []

    def process_pdf(self, response):
        """
        Descrizione: 
            Estrae il contenuto testuale di un PDF.
        
        Input:
            response: Oggetto Scrapy contenente il file PDF.
        
        Output:
            Stringa con il contenuto del PDF, oppure un messaggio di errore.
        
        Comportamento: 
            Utilizza PyPDF2 per leggere il contenuto del PDF.
        """
        try:
            pdf_file = BytesIO(response.body)
            reader = PyPDF2.PdfReader(pdf_file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
            return content
        except Exception as e:
            return f"Errore durante l'accesso al PDF: {e}"

    def parse(self, response):
        """
        Descrizione: 
            Estrae i link ai PDF da una pagina web.
        
        Input:
            response: Oggetto Scrapy contenente la risposta HTTP.
        
        Output:
            Generatore di richieste Scrapy per scaricare i PDF.
        
        Comportamento: 
            Cerca i link ai PDF all'interno di un div con classe page-content e li processa.
        """
        page_content_div = response.css('div.page-content').get()
        
        if not page_content_div:
            self.log("Nessun div.page-content trovato.")
            return

        # Crea una nuova risposta Scrapy solo con quel div
        partial_response = response.replace(body=page_content_div)

        # Ora estrae solo link dal contenuto del div
        links = partial_response.css('a')

        for link in links:
            title = ''.join(link.css('*::text').getall()).strip()
            url = link.css('::attr(href)').get()

            if url:
                full_url = response.urljoin(url)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.handle_file,
                    meta={'title': title}
                )
                


    def handle_file(self, response):
        """
        Descrizione: 
            Gestisce i file scaricati, estraendo il contenuto o salvando un messaggio generico.
        
        Input:
            response: Oggetto Scrapy contenente il file scaricato.
        
        Output:
            Nessuno (salva i dati estratti in una lista interna).
        
        Comportamento: 
            Determina il tipo di file e processa il contenuto se è un PDF.
        """
        title = response.meta['title']
        content_type = response.headers.get('Content-Type', b'').decode('utf-8')

        if "application/pdf" in content_type:
            # Processa il contenuto del PDF
            content = self.process_pdf(response)
        else:
            # Per altri tipi di file salva solo un messaggio generico
            content = f"File di tipo {content_type} scaricato."

        # Aggiungi i dati estratti alla lista
        self.extracted_data.append({
            'Titolo': title,
            'URL': response.url,
            'Contenuto': content
        })

    def closed(self, reason):
        """
        Descrizione: 
            Salva i dati estratti in un file JSON quando il crawler termina.
        
        Input:
            reason (str): Motivo della chiusura del crawler.
        
        Output:
            Nessuno (salva i dati in un file).
        
        Comportamento: 
            Scrive i dati estratti in dataScrapy.json.
        """
        with open('output/dataScrapy.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.extracted_data, jsonfile, ensure_ascii=False, indent=4)
        self.log("Dati salvati in 'dataScrapy.json'.")
