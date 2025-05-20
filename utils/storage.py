import os
import json

def append_result_to_file(path, nuovo_risultato):
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
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        os.remove(path)
