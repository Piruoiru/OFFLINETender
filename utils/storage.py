import os
import json

def append_result_to_file(path, nuovo_risultato):
    """
    Descrizione: 
        Aggiunge un nuovo risultato a un file JSON.
    
    Input:
        path (str): Percorso del file.
        nuovo_risultato (dict): Risultato da aggiungere.
    
    Output:
        Nessuno (modifica il file).
    
    Comportamento: 
        Legge il file, aggiunge il nuovo risultato e lo riscrive.
    """
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                dati = json.load(f)
                if not isinstance(dati, list):
                    dati = []
            except json.JSONDecodeError:
                dati = []
    else:
        dati = []

    dati.append(nuovo_risultato)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(dati, f, ensure_ascii=False, indent=4)

def reset_output_file(path):
    """
    Descrizione: 
        Resetta un file di output eliminandolo se esiste.
    
    Input:
        path (str): Percorso del file.
    
    Output:
        Nessuno.
    
    Comportamento: 
        Crea la directory se non esiste ed elimina il file.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
