import requests
import json
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import ollama

load_dotenv()

max_workers = int(os.getenv("MAX_WORKERS_PARALLEL_EMBEDDING"))

def get_embedding(text):
    """
    Genera l'embedding di un testo utilizzando il modello di embedding.
    
    Args:
        text (str): Il testo per cui generare l'embedding.
    
    Returns:
        list: L'embedding generato come lista di numeri.
    """
    model = os.getenv("MODEL_EMBEDDING")  
    url = os.getenv("MODEL_EMBEDDING_API") 
    # payload = {
    #     "model": model, 
    #     "prompt": text
    # }
    # headers = {
    #     "Content-Type": "application/json"
    # }
    response = ollama.embeddings(model=os.getenv("MODEL_EMBEDDING"), prompt=text)

    try:
        embedding = response.get("embedding")
        if embedding is None:
            raise ValueError("Embedding non trovato nella risposta.")
        return embedding
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta al server: {e}")
        return None
    except ValueError as e:
        print(f"Errore nella risposta del server: {e}")
        return None
    
def get_embeddings_parallel(texts, max_workers=max_workers):
    """
    Esegue embedding in parallelo su una lista di testi.
    """
    embeddings = [None] * len(texts)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(get_embedding, text): i for i, text in enumerate(texts)}
        
        for future in as_completed(futures):
            i = futures[future]
            try:
                result = future.result()
                embeddings[i] = result
            except Exception as e:
                print(f"[ERRORE] Chunk {i}: {e}")
                embeddings[i] = None

    return embeddings