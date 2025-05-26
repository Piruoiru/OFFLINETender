import os
import json
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def analyze_with_model(content):
    """
    Descrizione: 
        Analizza un testo utilizzando un modello LLM e restituisce i dati estratti in formato JSON.
    
    Input:
        content (str): Testo da analizzare.
    
    Output:
        Dizionario contenente i dati estratti o un messaggio di errore.
    
    Comportamento:
        Costruisce un prompt dettagliato con le istruzioni per il modello.
    
    Invia il prompt al modello LLM tramite API.
        Processa la risposta JSON e la restituisce.
    """
    try:
        user_input = (
            "Analizza il seguente testo e rispondi in formato JSON. Estrarre i seguenti dati, se presenti:\n"
            "- provider\n"
            "- publication_date\n"
            "- submission_deadline\n"
            "- procedure_title\n"
            "- purpose\n"
            "- funding_reference\n"
            "- cup\n"
            "- intervention_title\n"
            "- description\n"
            "- fund\n"
            "- required_characteristics\n"
            "- timelines\n"
            "- maximum_budget\n"
            "- deadline\n"
            "- email_for_quote\n"
            "- issuer_name\n"
            "- payment_method\n"
            "- company_relevance\n\n"
            "L'azienda si occupa di: 'Sviluppo siti web, consulenze informatiche, digitalizzazione, accessibilità, "
            "gestione server, sviluppo software, fornitura licenze software'. "
            "Valuta quanto il contenuto è pertinente rispetto a questo ambito. Fornisci una breve spiegazione o lascia vuoto se non pertinente.\n\n"
            "Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
            "Non includere oggetti JSON o dizionari come valori nei campi. Tutti i campi devono essere stringhe semplici.\n\n"
            "Non usare formati nidificati o array.\n\n"
            "Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
            f"Testo:\n{content}"
        )

        chat_completion = completion(
            messages=[{"role": "user", "content": user_input}],
            model=os.getenv("MODEL_LLM"),
            api_base=os.getenv("MODEL_LLM_API"),
            temperature=float(os.getenv("MODEL_TEMPERATURE")),
            max_tokens=int(os.getenv("MODEL_MAX_TOKENS")),
            timeout=1200
        )

        response = chat_completion["choices"][0]["message"]["content"]
        return process_llm_response(response)

    except Exception as e:
        print(f"Errore durante l'analisi: {e}")
        return {"error": str(e)}

def process_llm_response(response):
    """
    Descrizione: 
        Pulisce e converte la risposta del modello LLM in un oggetto JSON.
    
    Input:
        response (str): Risposta del modello LLM.
    
    Output:
        Dizionario JSON, oppure un messaggio di errore se la risposta non è valida.
    
    Comportamento: 
        Rimuove eventuali caratteri extra dalla risposta e tenta di decodificarla come JSON.
    """
    try:
        cleaned_response = response.strip().strip("```json").strip("```").strip()
        json_response = json.loads(cleaned_response)
        return json_response
    except json.JSONDecodeError:
        print("Errore: la risposta del modello non è un JSON valido.")
        return {"error": "Risposta del modello non valida", "raw": response}
    