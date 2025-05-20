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
        """
        Descrizione: 
            Esegue l'embedding di una lista di documenti utilizzando una funzione parallela.
        
        Input:
            texts (list): Lista di stringhe da trasformare in embedding.
        
        Output:
            Lista di vettori di embedding.
        
        Comportamento: 
            Utilizza la funzione get_embeddings_parallel per calcolare gli embedding in parallelo
        """
        return get_embeddings_parallel(texts)

    def embed_query(self, text):
        """
        Descrizione: 
            Esegue l'embedding di una singola query.
        
        Input:
            text (str): Testo della query da trasformare in embedding.
        
        Output:
            Un singolo vettore di embedding.
        
        Comportamento: 
            sChiama get_embeddings_parallel passando una lista con un solo elemento e restituisce il primo risultato.
        """
        return get_embeddings_parallel([text])[0]

def create_vectorstore(chunks):
    """
    Descrizione: 
        Crea un vectorstore FAISS a partire da una lista di chunk di testo.
    
    Input:
        chunks (list): Lista di stringhe rappresentanti i chunk di testo.
    
    Output:
        Un oggetto FAISS contenente i documenti e i loro embedding, oppure None in caso di errore.
    
    Comportamento: 
        Converte i chunk in oggetti Document, calcola gli embedding con CustomEmbedding e li salva in un vectorstore FAISS.
    """
    try:
        docs = [Document(page_content=chunk) for chunk in chunks]
        embedding_model = CustomEmbedding()
        return FAISS.from_documents(docs, embedding_model)
    except Exception as e:
        print(f"Errore durante la creazione del vectorstore: {e}")
        return None

def retrieve_top_k_chunks(vectorstore, query, k=similarity_k):
    """
    Descrizione:    
        Recupera i k chunk più simili a una query utilizzando il vectorstore.
    
    Input:
        vectorstore: Oggetto FAISS contenente i documenti e i loro embedding.
        query (str): Query di ricerca.
        k (int): Numero di risultati da restituire.
    
    Output:
        Lista dei documenti più simili alla query.
    
    Comportamento: 
        Utilizza la funzione similarity_search del vectorstore per trovare i chunk più rilevanti.
    """
    return vectorstore.similarity_search(query, k=k)

def analyze_with_retrieval(text, query="bando pubblico per digitalizzazione, sviluppo software e servizi IT", k=k_chunk_embedding_piu_simile_alla_query):
    """
    Descrizione: 
        Analizza un testo eseguendo chunking, embedding, retrieval semantico e analisi con un modello LLM.
    
    Input:
        text (str): Testo da analizzare.
        query (str): Query di ricerca (default: "bando pubblico per digitalizzazione, sviluppo software e servizi IT").
        k (int): Numero di chunk più simili da considerare.
    
    Output:
        Risultato dell'analisi del modello LLM.
    
    Comportamento:
        - Divide il testo in chunk.
        - Crea un vectorstore con gli embedding dei chunk.
        - Recupera i chunk più simili alla query.
        - Costruisce un prompt con i chunk rilevanti.
        - Invia il prompt al modello LLM per l'analisi.
        - Restituisce il risultato e stampa i tempi di esecuzione.
    """
    
    chunks = chunk_text(text)

    vectorstore = create_vectorstore(chunks)
    if vectorstore is None:
        raise RuntimeError("Vectorstore non creato.")
    top_chunks = retrieve_top_k_chunks(vectorstore, query=query, k=k)
    prompt = build_prompt_from_chunks(top_chunks)
    result = analyze_with_model(prompt)

    return result
