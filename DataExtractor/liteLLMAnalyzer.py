import os
import json
from litellm import completion
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_with_model(content):
    """
    Analizza il contenuto utilizzando il modello.
    
    Args:
        content (str): Il contenuto del documento da analizzare.
    
    Returns:
        dict: I dati estratti dal modello in formato JSON.
    """
    try:
        user_input = (
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

        chat_completion = completion(
            messages=[
                {"role": "user", "content": user_input}
            ],
            model=os.getenv("MODEL_LLM"),
            api_base=os.getenv("MODEL_LLM_API"),
            temperature=float(os.getenv("MODEL_TEMPERATURE")),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS")),
        )

        response = chat_completion["choices"][0]["message"]["content"]
        return process_llm_response(response)

    except Exception as e:
        print(f"Errore durante la richiesta al server: {e}")
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
        # Rimuovi eventuali delimitatori di codice e spazi bianchi
        cleaned_response = response.strip().strip("```json").strip("```").strip()

        json_response = json.loads(cleaned_response)
        return json_response   
    except json.JSONDecodeError:
        print("Errore: la risposta del modello non è un JSON valido.")
        print(cleaned_response)
        # print(json_response)
        return {}
            


