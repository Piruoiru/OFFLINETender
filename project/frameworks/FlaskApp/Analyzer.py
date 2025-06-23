from Project.Adapters.Auth.JwtHandler import generate_token, verify_token, get_token_from_request

from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import subprocess

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/.env"))
load_dotenv(dotenv_path)

app = Flask(__name__)

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("USERNAME_API")
    password = data.get("PASSWORD_API")

    if username == os.getenv("USERNAME_API") and password == os.getenv("PASSWORD_API"):
        token = generate_token(user_id=username)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenziali non valide"}), 401

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Autenticazione tramite token JWT
        token = get_token_from_request()
        verify_token(token)

        result = subprocess.run(
            ["python", "DataExtractor/main.py"], 
            capture_output=True, 
            text=True, 
        )
        return jsonify({
            "status": "done",
            "output": result.stdout,
            "error": result.stderr
        }), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout durante l'esecuzione di main.py"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)