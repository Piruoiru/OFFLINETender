import scrapy
from scrapy.crawler import CrawlerProcess
import PyPDF2
from io import BytesIO
from dotenv import load_dotenv
import os

# Lista globale per salvare i contenuti
extracted_pdfs = []

load_dotenv()

class PDFScraper(scrapy.Spider):
    name = "pdf_scraper"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = [os.environ["SITE_TO_SCRAPE"]]

    def process_pdf(self, response):
        try:
            pdf_file = BytesIO(response.body)
            reader = PyPDF2.PdfReader(pdf_file)
            content = ""
            for page in reader.pages:
                content += page.extract_text()
            return " ".join(content.split())
        except Exception as e:
            return f"Errore durante l'accesso al PDF: {e}"

    def parse(self, response):
        page_content_div = response.css('div.page-content').get()
        if not page_content_div:
            self.log("Nessun div.page-content trovato.")
            return

        partial_response = response.replace(body=page_content_div)
        links = partial_response.css('a')

        links = sorted(links, key=lambda l: l.css("::attr(href)").get() or "")

        for link in links:
            title = ''.join(link.css('*::text').getall()).strip()
            url = link.css('::attr(href)').get()

            if url and url.endswith(".pdf"):
                full_url = response.urljoin(url)
                yield scrapy.Request(
                    url=full_url,
                    callback=self.parse_pdf,
                    meta={'title': title}
                )

    def parse_pdf(self, response):
        title = response.meta.get("title", "senza_titolo")
        content = self.process_pdf(response)
        extracted_pdfs.append({
            "title": title,
            "content": content,
            "url": response.url
        })
