import requests
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import ollama

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/.env"))
load_dotenv(dotenv_path)

ollama.base_url = os.getenv("MODEL_EMBEDDING_API")

max_workers = int(os.getenv("MAX_WORKERS_PARALLEL_EMBEDDING"))
model = os.getenv("MODEL_EMBEDDING")  

def get_embeddings_parallel(texts, max_workers=max_workers):
    """
    Descrizione: 
        Esegue l'embedding di una lista di testi in parallelo.

    Input:
        texts (list): Lista di stringhe da trasformare in embedding.
        max_workers (int): Numero massimo di thread da utilizzare.

    Output:
        Lista di vettori di embedding.
    
    Comportamento: 
        Utilizza un pool di thread per calcolare gli embedding in parallelo chiamando la funzione get_embedding per ogni testo.
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
    """
    Descrizione: 
        Esegue una richiesta API per calcolare l'embedding di un singolo testo.

    Input:
        text (str): Testo da trasformare in embedding.

    Output:
        Vettore di embedding, oppure None in caso di errore.

    Comportamento: 
        Invia una richiesta POST all'API specificata, passando il testo come prompt.
    """
    url = os.getenv("MODEL_EMBEDDING_API") + "/api/embeddings"
    payload = {"model": model, "prompt": text}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        embedding = data.get("embedding")
        if not embedding or not isinstance(embedding, list):
            raise ValueError("Embedding non trovato o non valido nella risposta.")
        return embedding
    except Exception as e:
        print(f"Errore nella richiesta embedding: {e}")
        return None