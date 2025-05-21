import jwt
import datetime
from flask import request
from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)

def verify_token(token):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
        return decoded
    except jwt.ExpiredSignatureError:
        raise ValueError("Token scaduto.")
    except jwt.InvalidTokenError:
        raise ValueError("Token non valido.")

def get_token_from_request():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise ValueError("Token non trovato o malformato.")
    return auth_header[len("Bearer "):]
