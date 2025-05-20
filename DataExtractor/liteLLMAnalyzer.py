import os
import json
from flask import Flask, request, jsonify
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
            f"- Pertinenza con l'azienda\n\n"
            f"L'azienda si occupa di: 'Sviluppo siti web, consulenze informatiche, digitalizzazione, accessibilità, gestione server, sviluppo software, fornitura licenze software'. "
            f"Valuta quanto il contenuto è pertinente rispetto a questo ambito. Fornisci una breve spiegazione o lascia vuoto se non pertinente.\n\n"
            f"Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
            f"Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
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
        print(f"Errore durante la richiesta al server: {e}")
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
    
def build_prompt_from_chunks(chunks):
    """
    Descrizione: 
        Costruisce un prompt per il modello LLM unendo i chunk rilevanti.
    
    Input:
        chunks (list): Lista di oggetti Document contenenti i chunk di testo.
    
    Output:
        Stringa rappresentante il prompt.
    
    Comportamento: 
        Concatena i chunk e li aggiunge a un prompt base con istruzioni dettagliate.
    """
    base_prompt = (
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
        f"- Modalità di pagamento\n"
        f"- Pertinenza con l'azienda\n\n"
        f"L'azienda si occupa di: 'Sviluppo siti web, consulenze informatiche, digitalizzazione, accessibilità, gestione server, sviluppo software, fornitura licenze software'. "
        f"Valuta quanto il contenuto è pertinente rispetto a questo ambito. Fornisci una breve spiegazione o lascia vuoto se non pertinente.\n\n"
        f"Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
        f"Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
    )
    joined_chunks = "\n\n".join([doc.page_content for doc in chunks])
    return base_prompt + "Testo:\n" + joined_chunks