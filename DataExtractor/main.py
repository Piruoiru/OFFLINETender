from scrapy.crawler import CrawlerProcess
from scraperScrapy import PDFScraper, extracted_pdfs
from chunkizer import chunk_text
from embedderLocal import get_embeddings_parallel, get_embedding
from pgvector_utils import (
    insert_document, insert_response, retrieve_top_chunks_from_document,
    insert_sites, insert_chunks, get_document_id_by_hash, document_has_chunks, document_has_response
)
from liteLLMAnalyzer import analyze_with_model,build_user_input
from dotenv import load_dotenv
from hasher import generate_hash
from tokenizer import count_tokens
from insertStatisticDB import insert_statistics
import os
import json


load_dotenv()

if __name__ == "__main__":
    print("▶ Inizio del processo di scraping...")
    process = CrawlerProcess()
    process.crawl(PDFScraper)
    process.start()
    print("✅ Scraping completato.")

    for pdf in extracted_pdfs:
        doc_hash = generate_hash(pdf["url"])
        document_id = get_document_id_by_hash(doc_hash)

        if document_id:
            has_chunks = document_has_chunks(document_id)
            has_response = document_has_response(document_id)

            if has_chunks and has_response:
                print(f"⏩ Documento già completamente processato: {pdf['url']}")
                continue
            else:
                print(f"⚠️ Documento parzialmente processato: {pdf['url']}")
        else:
            site_url = os.environ["SITE_TO_SCRAPE"]
            site_id = insert_sites(site_url)
            print(f"🧠 Generazione Embedding del testo con ID: {document_id}")
            emdedding_document = get_embedding(pdf["content"]) #aggiunto questo
            document_id = insert_document(
                title=pdf["title"], url=pdf["url"], hash=doc_hash, site_id=site_id, document_embedding=emdedding_document
            )
            print(f"📥 Documento inserito con ID: {document_id}")
            has_chunks = False
            has_response = False

        print(f"\n📄 Elaborazione: {pdf['title']}")

        # Chunking ed embedding
        chunk_texts = chunk_text(pdf["content"])
        embeddings = get_embeddings_parallel(chunk_texts)
        print(f"🧠 Embeddings calcolati. Chunk generati: {len(chunk_texts)}")

        # Inserisci i chunk solo se non già presenti
        if not has_chunks:
            insert_chunks(chunk_texts, embeddings, document_id)
            print("📥 Chunks salvati.")
        else:
            print("ℹ️ Chunks già presenti, salto inserimento.")

        # Analisi LLM solo se mancante
        if not has_response:
            try:
                print("🔎 Selezione top chunk per il prompt...")
                top_k = min(10, len(chunk_texts))  # Assicurati che top_k non superi il numero di chunk
                top_chunks = retrieve_top_chunks_from_document(embeddings, chunk_texts, top_k=top_k)
                prompt = "\n\n".join(top_chunks)
                
                user_input = build_user_input(prompt)
                tokens_before = count_tokens(user_input)
                
                print("📤 Invio prompt al modello LLM...")
                llm_response = analyze_with_model(prompt)

                tokens_after = count_tokens(json.dumps(llm_response))

                # Se l'analisi ha fallito
                if not llm_response or "error" in llm_response:
                    print(f"❌ Errore nella risposta LLM: {llm_response.get('error') if isinstance(llm_response, dict) else 'Nessuna risposta'}")
                    continue

                print("✅ Risposta ricevuta. Salvataggio nel DB...")
                response_id = insert_response(llm_response, document_id=document_id)
                print(f"💾 Risposta salvata con ID: {response_id}")

                statistics_id = insert_statistics(document_id=document_id,token_prompt=tokens_before,token_response=tokens_after,prompt=json.dumps(user_input))
                print(f"📊 Statistiche salvate con ID: {statistics_id}")

            except Exception as e:
                print(f"❌ Eccezione durante analisi o salvataggio risposta: {e}")
                continue
        else:
            print("ℹ️ Risposta già presente, salto analisi.")

        print("✅ Aggiorna il numero di risposte LLM nella tabella statistics")
        