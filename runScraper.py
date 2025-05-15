import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from DataExtractor.scraperScrapy import PDFScraper

def run_scraper():
    process = CrawlerProcess(get_project_settings())
    process.crawl(PDFScraper)
    process.start()  # blocca fino a fine spider

if __name__ == "__main__":
    run_scraper()