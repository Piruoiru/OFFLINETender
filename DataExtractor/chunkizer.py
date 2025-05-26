from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()

chunk_size = int(os.getenv("CHUNK_SIZE"))
chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))

def chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap):
    """
    Divide il testo in chunk sovrapposti.

    Args:
        text (str): Il testo da dividere.
        chunk_size (int): Dimensione massima di ogni chunk.
        chunk_overlap (int): Sovrapposizione tra i chunk.

    Returns:
        list: Lista di stringhe, ognuna rappresenta un chunk.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)
