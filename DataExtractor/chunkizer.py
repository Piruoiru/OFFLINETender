import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedderLocal import get_embedding

def chunk_text(text, chunk_size=850, chunk_overlap=150):
    """
    Divide il testo in chunk sovrapposti.

    Args:
        text (str): Il testo da dividere.
        chunk_size (int): Dimensione massima di ogni chunk.
        chunk_overlap (int): Sovrapposizione tra i chunk.

    Returns:
        list: Lista di stringhe, ognuna rappresenta un chunk.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

if __name__ == "__main__":
    # Legge il file JSON generato da dataScrapy.py
    input_file = "../output/dataScrapy.json"
    output_file = "../output/dataChunkedWithEmbeddings.json"

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Verifica che il file JSON contenga un array di oggetti
        if not isinstance(data, list):
            raise ValueError("Il file JSON non contiene un array di oggetti.")

        # Genera i chunk e gli embedding per ogni oggetto
        output_data = []
        for item in data:
            titolo = item.get("Titolo", "Titolo non disponibile")
            url = item.get("URL", "URL non disponibile")
            contenuto = item.get("Contenuto", "")

            # Se il contenuto è vuoto, lascia i chunks vuoti
            if not contenuto.strip():
                chunks = []
                embeddings = []
            else:
                # Divide il contenuto in chunk
                chunks = chunk_text(contenuto, chunk_size=800, chunk_overlap=100)

                # Genera gli embedding per ogni chunk
                embeddings = []
                for chunk in chunks:
                    embedding = get_embedding(chunk)
                    embeddings.append(embedding)

            # Aggiunge l'oggetto con i chunk e gli embedding al risultato
            output_data.append({
                "Titolo": titolo,
                "URL": url,
                "chunks": chunks,
                "embeddings": embeddings
            })

        # Salva i dati con la nuova struttura in un file JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)

        print(f"File JSON con i chunk e gli embedding generato correttamente: {output_file}")
    except FileNotFoundError:
        print(f"Il file {input_file} non è stato trovato.")
    except json.JSONDecodeError:
        print("Errore nel decodificare il file JSON.")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")
