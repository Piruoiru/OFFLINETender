# import json
# from DataExtractor.embedderLocal import get_embedding

# def generate_embeddings_for_all_fields(input_file, output_file):
#     """
#     Legge un file JSON, genera un embedding per ogni campo di ogni elemento,
#     e aggiorna il file con gli embedding generati.

#     Args:
#         input_file (str): Il percorso del file JSON di input.
#         output_file (str): Il percorso del file JSON di output.
#     """
#     try:
#         # Leggi il file JSON di input
#         with open(input_file, 'r', encoding='utf-8') as infile:
#             data = json.load(infile)

#         for entry in data:
#             # Itera su una copia delle chiavi del dizionario
#             for key in list(entry.keys()):
#                 value = entry[key]
#                 # Genera un embedding solo per i campi di tipo stringa
#                 if isinstance(value, str) and value.strip():
#                     print(f"Generazione embedding per il campo '{key}'...")
#                     try:
#                         embedding = get_embedding(value)
#                         entry[f"{key}_Embedding"] = embedding  # Salva l'embedding con un nuovo campo
#                     except Exception as e:
#                         print(f"Errore durante la generazione dell'embedding per il campo '{key}': {e}")
#                         entry[f"{key}_Embedding"] = None  # Imposta a None in caso di errore

#         # Salva il file JSON aggiornato
#         with open(output_file, 'w', encoding='utf-8') as outfile:
#             json.dump(data, outfile, ensure_ascii=False, indent=4)

#         print(f"File aggiornato salvato in: {output_file}")

#     except FileNotFoundError:
#         print(f"Errore: Il file '{input_file}' non è stato trovato.")
#     except json.JSONDecodeError:
#         print(f"Errore: Il file '{input_file}' non è un JSON valido.")
#     except Exception as e:
#         print(f"Errore durante l'elaborazione: {e}")