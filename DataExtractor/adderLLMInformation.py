import json
from DataExtractor.liteLLMAnalyzer import analyze_with_model

def add_information_to_json(input_file, output_file):
    """
    Legge i dati da un file JSON, aggiunge embedding e informazioni dal modello,
    e salva il risultato in un nuovo file JSON.

    Args:
        input_file (str): Il percorso del file JSON di input.
        output_file (str): Il percorso del file JSON di output.
    """
    try:
        # Leggi i dati dal file JSON di input
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)

        # Itera sui dati e aggiungi embedding e analisi del modello
        enriched_data = []
        for entry in data:
            content = entry.get('Contenuto', None)

            model_analysis = {}
            if content:
                try:
                    model_analysis = analyze_with_model(content)
                except Exception as e:
                    print(f"Errore durante l'analisi con il modello: {e}")

            # Struttura i dati finali
            enriched_entry = {
                "Titolo": entry.get("Titolo", ""),
                "URL": entry.get("URL", ""),
                "Contenuto": content,
                **model_analysis 
            }

            # Aggiungi l'entry arricchita alla lista
            enriched_data.append(enriched_entry)

        # Salva i dati aggiornati nel file di output
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(enriched_data, outfile, ensure_ascii=False, indent=4)

        print(f"Dati aggiornati salvati in '{output_file}'.")

    except FileNotFoundError:
        print(f"Errore: Il file '{input_file}' non è stato trovato.")
    except json.JSONDecodeError:
        print(f"Errore: Il file '{input_file}' non è un JSON valido.")
    except Exception as e:
        print(f"Errore durante l'elaborazione: {e}")


# Esegui la funzione
# if __name__ == "__main__":
#     input_file = "dataScrapy.json"
#     output_file = "dataAddedInformation.json"
#     add_information_to_json(input_file, output_file)