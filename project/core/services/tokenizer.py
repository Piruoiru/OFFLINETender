import tiktoken
import os
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config/.env"))
load_dotenv(dotenv_path)

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
    


