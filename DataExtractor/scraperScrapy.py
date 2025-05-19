import scrapy
from scrapy.crawler import CrawlerProcess
import json
import PyPDF2
from io import BytesIO
from dotenv import load_dotenv
import os

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
        """Analizza la pagina principale e trova i link ai file PDF."""
        data_section = response.css('div.page-content')
        if data_section:
            links = data_section.css('a')

            for link in links:
                # Estraggo tutto il testo compreso quello nidificato
                title = ''.join(link.css('*::text').getall()).strip()
                url = link.css('::attr(href)').get()

                if url:
                    # Controlla se ci sono altri URL all'interno di altri URL
                    full_url = response.urljoin(url)

                    # Scarica tutti i file indipendentemente dal tipo
                    yield scrapy.Request(
                        url=full_url,
                        callback=self.handle_file,
                        meta={'title': title}
                    )
        else:
            self.log("Sezione dati non trovata.")

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