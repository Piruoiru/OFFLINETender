# from chunkizer import chunk_text
# from embedderLocal import get_embeddings_parallel
# import PyPDF2
# from io import BytesIO
# import hashlib
# from pgvector_utils import insert_pdf_link_to_site_table, insert_chunk
# from liteLLMAnalyzer import analyze_with_model
# from pgvector_utils import insert_response, normalize_llm_response


# def handle_file(response):
#     """
#     Estrae testo da un PDF, lo divide in chunk, genera embedding e salva nel DB.
#     """
#     url = response.url
#     title = response.meta.get("title", "Senza titolo")

#     # Estrazione del contenuto del PDF
#     try:
#         pdf_file = BytesIO(response.body)
#         reader = PyPDF2.PdfReader(pdf_file)
#         content = ""
#         for page in reader.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 content += page_text + "\n"
#     except Exception as e:
#         print(f"Errore durante la lettura del PDF da {url}: {e}")
#         return

#     # Normalizzazione base
#     content = " ".join(content.split())

#     if not content:
#         print(f"Nessun contenuto estratto dal PDF: {url}")
#         return

#     # Chunking del testo
#     chunks = chunk_text(content)
#     if not chunks:
#         print(f"Nessun chunk generato per il PDF: {url}")
#         return

#     # Calcolo degli embedding
#     embeddings = get_embeddings_parallel(chunks)

#     # Inserimento nel DB
#     site_id = insert_pdf_link_to_site_table(url, title=title)

#     for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
#         if not embedding:
#             print(f"Skipping chunk {i} per errore di embedding.")
#             continue

#         chunk_id = hashlib.md5(f"{url}_chunk_{i}".encode("utf-8")).hexdigest()

#         insert_chunk(
#             title=title,
#             url=url,
#             chunk=chunk,
#             embedding=embedding,
#             site_id=site_id,
#             chunk_id=chunk_id
#         )

#     print(f"Completato: {title} ({len(chunks)} chunk)")

    

