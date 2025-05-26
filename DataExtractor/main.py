from scrapy.crawler import CrawlerProcess
from scraperScrapy import PDFScraper, extracted_pdfs
from chunkizer import chunk_text
from embedderLocal import get_embeddings_parallel
from pgvector_utils import insert_document, insert_response, retrieve_top_chunks_from_document, insert_sites, insert_chunks
from liteLLMAnalyzer import analyze_with_model
from dotenv import load_dotenv
import os

load_dotenv()

processed=set()

if __name__ == "__main__":
    print("▶ Inizio del processo di scraping...")
    process = CrawlerProcess()
    process.crawl(PDFScraper)
    process.start()
    print("✅ Scraping completato.")

    for pdf in extracted_pdfs:
        print(f"\n📄 Elaborazione: {pdf['title']}")
        chunk_texts = chunk_text(pdf["content"])
        print(f"➡️ Chunk generati: {len(chunk_texts)}")

        embeddings = get_embeddings_parallel(chunk_texts)
        print("🧠 Embeddings calcolati.")

        site_url = os.environ["SITE_TO_SCRAPE"]
        site_id = insert_sites(site_url)

        # ✅ Inserisce ogni documento nel DB
        document_id = insert_document(title=pdf["title"],url=pdf["url"],site_id=site_id)
        print(f"📥 Documento salvato con ID: {document_id}")

        # ✅ Inserise ogni chunk nel DB nella tabella `chunks`
        insert_chunks(chunk_texts, embeddings, document_id)
        print(f"📥 Chunks salvati")


        # 🔎 Recupera i 5 chunk più rappresentativi tra quelli appena inseriti
        top_chunks = retrieve_top_chunks_from_document(embeddings, chunk_texts, top_k=5)
        prompt = "\n\n".join(top_chunks)

        # 📊 Analisi LLM
        llm_response = analyze_with_model(prompt)
        print("🧾 Analisi completata.")

        # 💾 Salva la risposta nel DB
        response_id = insert_response(llm_response, document_id=document_id)
        print(f"💾 Risposta salvata con ID: {response_id}")

