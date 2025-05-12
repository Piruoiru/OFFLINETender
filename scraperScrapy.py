	
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import PyPDF2
from io import BytesIO
import re

class PDFScraper(scrapy.Spider):
    name = "pdf_scraper"
    start_urls = [
        "https://noi.bz.it/it/chi-siamo/societa-trasparente/bandi-di-gara-e-contratti/avvisi-e-indagini-di-mercato"
    ]

    extracted_data = []

    def extract_provider(self, text):
        """Estrae il provider dal testo utilizzando pattern predefiniti e fallback."""
        # Pattern specifici per individuare il provider
        patterns = [
            r'([A-Z][A-Za-z\s\.&-]+(?:S\.p\.A\.|S\.r\.l\.|Società|Associazione|Ente))\s+intende individuare',
            r'([A-Z][A-Za-z\s\.&-]+(?:S\.p\.A\.|S\.r\.l\.))\s+(?:indice|pubblica)',
            r'La\s+([A-Z][A-Za-z\s\.&-]+)\s+(?:intende|ricerca|lancia)',
            r'([A-Z][A-Za-z\s\.&-]+(?:S\.p\.A\.|S\.r\.l\.))', 
        ]

        # Cerco i provider nei pattern definiti sopra
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1).strip()

        # Cerco attraverso parole chiave che fornisco io e vanno nel fallback
        keywords = ["S.p.A.", "Associazione", "Società", "S.r.l.", "Ente"]
        for keyword in keywords:
            if keyword in text:
                return keyword

        return "Provider non trovato"

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
        data_section = response.css('div.content')
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

        # Estrai il provider dal contenuto o dal titolo
        provider = self.extract_provider(content if content else title)

        # Aggiungi i dati estratti alla lista
        self.extracted_data.append({
            'Titolo': title,
            'URL': response.url,
            'Contenuto': content,
            'Provider': provider
        })

    def closed(self, reason):
        """Salva i dati estratti quando il crawler termina."""
        with open('dataScrapy.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(self.extracted_data, jsonfile, ensure_ascii=False, indent=4)
        self.log("Dati salvati in 'dataScrapy.json'.")

# Esegui il crawler
process = CrawlerProcess()
process.crawl(PDFScraper)
process.start()