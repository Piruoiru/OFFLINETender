import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

class LLMResponseService:
    def __init__(self, model=None):
        self.model = os.getenv("MODEL_LLM")

    def get_LLM_response(content):
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
            user_input = user_input

            chat_completion = completion(
                messages=[{"role": "user", "content": user_input}],
                model=os.getenv("MODEL_LLM"),
                api_base=os.getenv("MODEL_LLM_API"),
                temperature=float(os.getenv("MODEL_TEMPERATURE")),
                max_tokens=int(os.getenv("MODEL_MAX_TOKENS")),
            )

            response = chat_completion["choices"][0]["message"]["content"]

        except Exception as e:
            print(f"Errore durante l'analisi: {e}")
            return {"error": str(e)}