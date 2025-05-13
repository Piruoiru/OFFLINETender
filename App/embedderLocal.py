import requests
import json

def get_embedding(text):
    """
    Genera l'embedding di un testo utilizzando il modello di embedding di Ollama.
    
    Args:
        text (str): Il testo per cui generare l'embedding.
    
    Returns:
        list: L'embedding generato come lista di numeri.
    """
    url = "http://app:11434/api/embeddings"  # Endpoint del server Ollama
    payload = {
        "model": "mxbai-embed-large",  # Nome del modello di embedding
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
        print(f"Errore durante la richiesta al server Ollama: {e}")
        return None
    except ValueError as e:
        print(f"Errore nella risposta del server Ollama: {e}")
        return None
