# from scrapy.crawler import CrawlerProcess
# from scraperScrapy import PDFScraper, extracted_pdfs
# from chunkizer import chunk_text
# from embedderLocal import get_embeddings_parallel
# from pgvector_utils import insert_document_chunks, insert_response, retrieve_top_chunks_from_document, insert_sites
# from liteLLMAnalyzer import analyze_with_model
# from dotenv import load_dotenv
# import os

# load_dotenv()

# processed=set()

# if __name__ == "__main__":
#     print("▶ Inizio del processo di scraping...")
#     process = CrawlerProcess()
#     process.crawl(PDFScraper)
#     process.start()
#     print("✅ Scraping completato.")

#     for pdf in extracted_pdfs:
#         print(f"\n📄 Elaborazione: {pdf['title']}")
#         chunk_texts = chunk_text(pdf["content"])
#         print(f"➡️ Chunk generati: {len(chunk_texts)}")

#         embeddings = get_embeddings_parallel(chunk_texts)
#         print("🧠 Embeddings calcolati.")

#         site_url = os.environ["SITE_TO_SCRAPE"]
#         site_id = insert_sites(site_url)

#         # ✅ Inserisce ogni chunk nel DB
#         document_id = insert_document_chunks(
#             title=pdf["title"],
#             url=pdf["url"],
#             chunks=chunk_texts,
#             embeddings=embeddings,
#             site_id=site_id,
#         )
#         print("📥 Chunk e embedding salvati in DB.")

#         # 🔎 Recupera i 5 chunk più rappresentativi tra quelli appena inseriti
#         top_chunks = retrieve_top_chunks_from_document(embeddings, chunk_texts, top_k=5)
#         prompt = "\n\n".join(top_chunks)

#         # 📊 Analisi LLM
#         llm_response = analyze_with_model(prompt)
#         print("🧾 Analisi completata.")

#         # 💾 Salva la risposta nel DB
#         response_id = insert_response(llm_response, document_id=document_id)
#         print(f"💾 Risposta salvata con ID: {response_id}")


import time
from scraperScrapy import PDFScraper, extracted_pdfs
from scrapy.crawler import CrawlerProcess
from threading import Thread
from chunkizer import chunk_text
from embedderLocal import get_embeddings_parallel
from pgvector_utils import insert_document_chunks, insert_response, retrieve_top_chunks_from_document, insert_sites
from liteLLMAnalyzer import analyze_with_model
from dotenv import load_dotenv
import os

load_dotenv()
processed = set()  # Per evitare duplicati

def process_pdf(pdf):
    print(f"\n📄 Elaborazione: {pdf['title']}")
    chunk_texts = chunk_text(pdf["content"])
    print(f"➡️ Chunk generati: {len(chunk_texts)}")

    embeddings = get_embeddings_parallel(chunk_texts)
    print("🧠 Embeddings calcolati.")

    site_url = os.environ["SITE_TO_SCRAPE"]
    site_id = insert_sites(site_url)

    document_id = insert_document_chunks(
        title=pdf["title"],
        url=pdf["url"],
        chunks=chunk_texts,
        embeddings=embeddings,
        site_id=site_id,
    )
    print("📥 Chunk e embedding salvati in DB.")

    top_chunks = retrieve_top_chunks_from_document(embeddings, chunk_texts, top_k=5)
    prompt = "\n\n".join(top_chunks)

    llm_response = analyze_with_model(prompt)
    print("🧾 Analisi completata.")

    response_id = insert_response(llm_response, document_id=document_id)
    print(f"💾 Risposta salvata con ID: {response_id}")

def watch_extracted_pdfs():
    while True:
        for pdf in extracted_pdfs:
            key = (pdf["title"], pdf["url"])
            if key not in processed:
                process_pdf(pdf)
                processed.add(key)
        time.sleep(2)  # Intervallo di polling

if __name__ == "__main__":
    print("▶ Inizio scraping asincrono...")

    # Avvia il thread che monitora e processa i PDF in tempo reale
    Thread(target=watch_extracted_pdfs, daemon=True).start()

    # Avvia lo scraper
    process = CrawlerProcess()
    process.crawl(PDFScraper)
    process.start()

    print("✅ Scraping completato.")
