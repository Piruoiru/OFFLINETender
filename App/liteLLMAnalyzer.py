# import os
# import json
# from dotenv import load_dotenv
# from litellm import completion


# load_dotenv()
# # Carica la chiave API di OpenAI dalle variabili d'ambiente
# os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"


# def analyze_with_llama(content):
#     """
#     Analizza il contenuto utilizzando il modello Llama tramite l'API di Groq.
    
#     Args:
#         content (str): Il contenuto del documento da analizzare.
    
#     Returns:
#         dict: I dati estratti dal modello Llama in formato JSON.
#     """
#     try:
#         # Prompt per il modello
#         user_input = (
#             f"Analizza il seguente testo e rispondi in formato JSON. Estrarre i seguenti dati, se presenti:\n"
#             f"- Provider (nome dell'organizzazione o azienda)\n"
#             f"- Data di pubblicazione\n"
#             f"- Data di termine di consegna\n"
#             f"- Tipologia di procedura\n"
#             f"- Finalità\n"
#             f"- Riferimento finanziamento\n"
#             f"- CUP\n"
#             f"- Titolo dell'intervento\n"
#             f"- Descrizione\n"
#             f"- Fondo\n"
#             f"- Caratteristiche richieste\n"
#             f"- Tempistiche\n"
#             f"- Budget massimo\n"
#             f"- Deadline\n"
#             f"- Mail a cui mandare la quota\n"
#             f"- Nome emittente\n"
#             f"- Modalità di pagamento\n\n"
#             f"Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
#             f"Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
#             f"Testo:\n{content}"
#         )

#         chat_completion = completion(
#             messages=[
#                 {"role": "user", "content": user_input}
#             ],
#             model="openai/gpt-3.5-turbo",
#             temperature=0.7,
#             max_tokens=1000,
#         )

#         # Estrai la risposta dal modello
#         response = chat_completion["choices"][0]["message"]["content"]

#         # Elabora la risposta e convertila in JSON
#         return process_llm_response(response)

#     except Exception as e:
#         print(f"Errore durante la richiesta al server Groq: {e}")
#         return {}

# def process_llm_response(response):
#     """
#     Elabora la risposta grezza del modello e la converte in un JSON valido.

#     Args:
#         response (str): La risposta grezza del modello.

#     Returns:
#         dict: Un dizionario Python con i dati estratti, oppure un dizionario vuoto in caso di errore.
#     """
#     try:
#         # Prova a caricare la risposta come JSON
#         json_response = json.loads(response)
#         return json_response
#     except json.JSONDecodeError:
#         print("Errore: La risposta del modello non è un JSON valido.")
#         # Tentativo di pulire la risposta
#         try:
#             # Rimuovi caratteri extra come backticks e spazi
#             cleaned_response = response.strip().strip("```").strip()
#             json_response = json.loads(cleaned_response)
#             return json_response
#         except json.JSONDecodeError:
#             print("Errore: Impossibile correggere la risposta del modello.")
#             return {}


