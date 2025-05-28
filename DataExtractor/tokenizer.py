import tiktoken
from dotenv import load_dotenv
import os

load_dotenv()

model = os.getenv("MODEL_LLM")


def count_tokens(text) -> int:
    """
    Conta il numero di token in un testo per un dato modello LLM.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))
    


