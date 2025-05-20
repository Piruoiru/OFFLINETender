import os
import json
import time
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.docstore.document import Document
from DataExtractor.embedderLocal import get_embeddings_parallel
from DataExtractor.chunkizer import chunk_text
from DataExtractor.liteLLMAnalyzer import build_prompt_from_chunks, analyze_with_model

load_dotenv()

similarity_k = int(os.getenv("SIMILARITY_K", 4))
k_chunk_embedding_piu_simile_alla_query = int(os.getenv("K_CHUNK_EMBEDDING_PIU_SIMILE_ALLA_QUERY", 4))

class CustomEmbedding(Embeddings):
    def embed_documents(self, texts):
        return get_embeddings_parallel(texts)

    def embed_query(self, text):
        return get_embeddings_parallel([text])[0]

def create_vectorstore(chunks):
    try:
        docs = [Document(page_content=chunk) for chunk in chunks]
        embedding_model = CustomEmbedding()
        return FAISS.from_documents(docs, embedding_model)
    except Exception as e:
        print(f"Errore durante la creazione del vectorstore: {e}")
        return None

def retrieve_top_k_chunks(vectorstore, query, k=similarity_k):
    return vectorstore.similarity_search(query, k=k)

def analyze_with_retrieval(text, query="bando pubblico per digitalizzazione, sviluppo software e servizi IT", k=k_chunk_embedding_piu_simile_alla_query):
    """
    Analizza un testo eseguendo:
    - chunking
    - embedding parallelo
    - retrieval semantico
    - costruzione prompt
    - invio a LLM
    """
    timers = {}

    chunks = chunk_text(text)

    t0 = time.time()
    vectorstore = create_vectorstore(chunks)
    timers["Embedding"] = round(time.time() - t0, 2)

    if vectorstore is None:
        raise RuntimeError("Vectorstore non creato.")

    t1 = time.time()
    top_chunks = retrieve_top_k_chunks(vectorstore, query=query, k=k)
    timers["Retrieval"] = round(time.time() - t1, 2)

    prompt = build_prompt_from_chunks(top_chunks)

    t2 = time.time()
    result = analyze_with_model(prompt)
    timers["LLM"] = round(time.time() - t2, 2)

    timers["Totale"] = round(sum(timers.values()), 2)

    print("\n📊 [TEMPI DETTAGLIATI]")
    for fase, sec in timers.items():
        print(f"  ➤ {fase}: {sec} sec")

    return result
