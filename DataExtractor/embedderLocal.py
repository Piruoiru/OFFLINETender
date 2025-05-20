import requests
import json
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import ollama

load_dotenv()

ollama.base_url = os.getenv("MODEL_EMBEDDING_API")

max_workers = int(os.getenv("MAX_WORKERS_PARALLEL_EMBEDDING"))
model = os.getenv("MODEL_EMBEDDING")  

# def get_embedding(text):
#     """
#     Genera l'embedding di un testo utilizzando il modello di embedding.
    
#     Args:
#         text (str): Il testo per cui generare l'embedding.
    
#     Returns:
#         list: L'embedding generato come lista di numeri.
#     """
#     # url = os.getenv("MODEL_EMBEDDING_API") 
#     # payload = {
#     #     "model": model, 
#     #     "prompt": text
#     # }
#     # headers = {
#     #     "Content-Type": "application/json"
#     # }
#     response = ollama.embeddings(model=model, prompt=text)

#     try:
#         embedding = response.get("embedding")
#         if embedding is None:
#             raise ValueError("Embedding non trovato nella risposta.")
#         return embedding
#     except ValueError as e:
#         print(f"Errore nella risposta del server: {e}")
#         return None
    
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

def get_embedding(text):
    url = os.getenv("MODEL_EMBEDDING_API") + "/api/embeddings"
    payload = {"model": model, "prompt": text}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        embedding = data.get("embedding")
        if embedding is None:
            raise ValueError("Embedding non trovato nella risposta.")
        return embedding
    except Exception as e:
        print(f"Errore nella richiesta embedding: {e}")
        return None