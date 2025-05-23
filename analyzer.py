# # from flask import Flask, request, Response, stream_with_context
# # from dotenv import load_dotenv
# # import os, json
# # from controller import generate_analysis_stream
# # from utils.storage import reset_output_file
# # from auth.jwt_handler import get_token_from_request, verify_token, generate_token
# # import os

# # load_dotenv()
# # analyzer = Flask(__name__)
# # output_path = "output/dataAnalyzed.json"

# # @analyzer.route("/login", methods=["POST"])
# # def login():
# #     data = request.get_json()
# #     if data.get("username") == os.getenv("USERNAME_API") and data.get("password") == os.getenv("PASSWORD_API"):
# #         token = generate_token(user_id=1)
# #         return {"token": token}
# #     return {"error": "Credenziali invalide"}, 401

# # @analyzer.route("/analyze", methods=["POST"])
# # def stream_analysis():
# #     """
# #     Descrizione: 
# #         Endpoint Flask per avviare l'analisi e restituire i risultati in streaming.
    
# #     Input:
# #         Richiesta HTTP contenente un JSON con il campo url.
    
# #     Output:
# #         Stream di risultati JSON.
    
# #     Comportamento:
# #         Legge l'URL dalla richiesta.
# #         Resetta il file di output.
# #         Avvia il crawler e restituisce i risultati in streaming.
# #     """
# #     try:
# #         token = get_token_from_request()
# #         user = verify_token(token)
# #     except ValueError as e:
# #         return Response(json.dumps({"error": str(e)}), status=401)
    
# #     data = request.get_json()
# #     if not data or "url" not in data:
# #         return Response(json.dumps({"error": "Fornire 'url': 'https://...'"}, ensure_ascii=False), status=400)

# #     os.environ["SITE_TO_SCRAPE"] = data["url"]
# #     reset_output_file(output_path)
# #     # print("[DEBUG] Flask usa MODEL_LLM_API =", os.getenv("MODEL_LLM_API"))

# #     return Response(
# #         stream_with_context(generate_analysis_stream(output_path)),
# #         mimetype='application/json'
# #     )

# # if __name__ == "__main__":
# #     analyzer.run(host="0.0.0.0", port=5000)

# from flask import Flask, request, Response, stream_with_context
# from dotenv import load_dotenv
# import os, json, requests
# from controller import generate_analysis_stream
# from auth.jwt_handler import get_token_from_request, verify_token, generate_token

# load_dotenv()
# analyzer = Flask(__name__)
# output_path = "output/dataAnalyzed.json"

# SAVE_DATA_URL = os.getenv("SAVE_DATA_URL", "http://saver:5001/save-data")  # fallback utile in Docker

# @analyzer.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     if data.get("username") == os.getenv("USERNAME_API") and data.get("password") == os.getenv("PASSWORD_API"):
#         token = generate_token(user_id=1)
#         return {"token": token}
#     return {"error": "Credenziali invalide"}, 401

# @analyzer.route("/analyze", methods=["POST"])
# def stream_analysis():
#     """
#     Descrizione: 
#         Avvia l'analisi del sito fornito e restituisce i risultati in streaming.
#         Alla fine salva i dati nel database chiamando l'API /save-data.
#     """
#     try:
#         token = get_token_from_request()
#         verify_token(token)
#     except ValueError as e:
#         return Response(json.dumps({"error": str(e)}), status=401)

#     data = request.get_json()
#     if not data or "url" not in data:
#         return Response(json.dumps({"error": "Fornire 'url': 'https://...'"}, ensure_ascii=False), status=400)

#     os.environ["SITE_TO_SCRAPE"] = data["url"]
#     # reset_output_file(output_path)

#     def generate_and_save():
#         for chunk in generate_analysis_stream(output_path):
#             yield chunk
#         # Avvisiamo il client che l'analisi è finita e parte il salvataggio
#         yield json.dumps({"info": "Analisi completata. Salvataggio nel database..."}, ensure_ascii=False) + "\n"

#         try:
#             response = requests.post(SAVE_DATA_URL)
#             result = response.json()
#             yield json.dumps(result, ensure_ascii=False) + "\n"
#         except Exception as e:
#             yield json.dumps({"error": f"Errore durante il salvataggio nel DB: {str(e)}"}, ensure_ascii=False) + "\n"

#     return Response(
#         stream_with_context(generate_and_save()),
#         mimetype='application/json'
#     )

# if __name__ == "__main__":
#     analyzer.run(host="0.0.0.0", port=5000)
