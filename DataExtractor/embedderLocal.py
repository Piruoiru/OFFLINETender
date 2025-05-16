import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

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
    payload = {
        "model": model, 
        "prompt": text
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP
        embedding = response.json().get("embedding")
        if embedding is None:
            raise ValueError("Embedding non trovato nella risposta.")
        return embedding
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta al server: {e}")
        return None
    except ValueError as e:
        print(f"Errore nella risposta del server: {e}")
        return None