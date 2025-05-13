import requests
import json

def analyze_with_llama(content):
    """
    Analizza il contenuto utilizzando il modello Llama tramite il server Ollama.

    Args:
        content (str): Il contenuto del documento da analizzare.

    Returns:
        dict: I dati estratti dal modello Llama in formato JSON.
    """
    url = "http://localhost:11435/api/completions"  # Endpoint per completamenti di testo
    payload = {
        "model": "llama3.1",  # Nome del modello
        "prompt": (
            f"Analizza il seguente testo e rispondi in formato JSON. Estrarre i seguenti dati, se presenti:\n"
            f"- Provider (nome dell'organizzazione o azienda)\n"
            f"- Data di pubblicazione\n"
            f"- Data di termine di consegna\n"
            f"- Tipologia di procedura\n"
            f"- Finalità\n"
            f"- Riferimento finanziamento\n"
            f"- CUP\n"
            f"- Titolo dell'intervento\n"
            f"- Descrizione\n"
            f"- Fondo\n"
            f"- Caratteristiche richieste\n"
            f"- Tempistiche\n"
            f"- Budget massimo\n"
            f"- Deadline\n"
            f"- Mail a cui mandare la quota\n"
            f"- Nome emittente\n"
            f"- Modalità di pagamento\n\n"
            f"Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
            f"Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
            f"Testo:\n{content}"
        )
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP

        # Estrai la risposta dal server
        response_data = response.json()
        if "completion" in response_data:
            return process_llm_response(response_data["completion"])
        else:
            print("Errore: Nessun campo 'completion' trovato nella risposta.")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"Errore durante la richiesta al server Ollama: {e}")
        return {}
    except ValueError as e:
        print(f"Errore nella risposta del server Ollama: {e}")
        return {}

def process_llm_response(response):
    """
    Elabora la risposta grezza del modello e la converte in un JSON valido.

    Args:
        response (str): La risposta grezza del modello.

    Returns:
        dict: Un dizionario Python con i dati estratti, oppure un dizionario vuoto in caso di errore.
    """
    try:
        # Prova a caricare la risposta come JSON
        json_response = json.loads(response)
        return json_response
    except json.JSONDecodeError:
        print("Errore: La risposta del modello non è un JSON valido.")
        return {}