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
    start_urls =[os.getenv("SITE_TO_SCRAPE")]

    extracted_data = []

    def process_pdf(self, response):
        """Legge il contenuto di un PDF direttamente dalla risposta."""
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
        """Estrae solo i link PDF dal div con class='page-content'."""
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
        """Gestisce i file scaricati in memoria."""
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
        """Salva i dati estratti quando il crawler termina."""
        with open('output/dataScrapy.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.extracted_data, jsonfile, ensure_ascii=False, indent=4)
        self.log("Dati salvati in 'dataScrapy.json'.")
