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
from handler import handle_file as process_and_store_pdf

load_dotenv()

class PDFScraper(scrapy.Spider):
    name = "pdf_scraper"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [os.environ["SITE_TO_SCRAPE"]] 

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
                callback=process_and_store_pdf,
                meta={'title': title}
            )
