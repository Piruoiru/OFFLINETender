import json
from embedder import get_embedding

def load_existing_data(filepath):
    """Carica i dati esistenti dal file JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Se il file non esiste, ritorna una lista vuota

def save_data(new_data, filepath='dataScrapy.json'):
    """
    Salva i dati nel file JSON, aggiungendo gli embeddings.
    
    Args:
        new_data (list): Lista di nuovi dati da salvare.
        filepath (str): Percorso del file JSON.
    """
    # Carica i dati esistenti
    existing_data = load_existing_data(filepath)

    # Aggiungi gli embeddings ai nuovi dati
    for item in new_data:
        item['Embedding'] = get_embedding(item.get('Contenuto', ''))

    # Unisci i dati esistenti con i nuovi
    updated_data = existing_data + new_data

    # Salva i dati aggiornati nel file JSON
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)

    print(f"Dati salvati in '{filepath}'.")