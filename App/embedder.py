from openai import OpenAI
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=api_key)

def get_embedding():
    """
    Ottiene un embedding per il testo fornito utilizzando il modello text-embedding-ada-002.
    """
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input="cat",
    )