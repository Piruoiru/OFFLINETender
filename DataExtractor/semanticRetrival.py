import os
import json
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from DataExtractor.embedderLocal import get_embedding
from litellm import completion

load_dotenv()

from DataExtractor.chunkizer import chunk_text

def create_vectorstore(chunks):
    """
    Crea un vectorstore FAISS dai chunk di testo forniti.

    Args:
        chunks (list): Lista di stringhe, ognuna rappresenta un chunk di testo.

    Returns:
        FAISS: Un vectorstore FAISS contenente i documenti e i relativi embedding.
    """
    try:
        # Crea i documenti dai chunk
        docs = [Document(page_content=chunk) for chunk in chunks]

        # Genera gli embedding per ogni chunk
        embeddings = []
        for chunk in chunks:
            embedding = get_embedding(chunk)  # Usa la funzione get_embedding per ogni chunk
            if embedding is None:
                raise ValueError(f"Errore nella generazione dell'embedding per il chunk: {chunk}")
            embeddings.append(embedding)

        # Crea il vectorstore FAISS dai documenti e dagli embedding
        vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings(embeddings))

        return vectorstore
    except Exception as e:
        print(f"Errore durante la creazione del vectorstore: {e}")
        return None

def retrieve_top_k_chunks(vectorstore, query, k=4):
    return vectorstore.similarity_search(query, k=k)

def build_prompt_from_chunks(chunks):
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
        f"- Modalità di pagamento\n\n"
        f"- Pertinenza con l'azienda: Valuta quanto il contenuto del testo è pertinente con l'attività dell'azienda. "
        f"L'azienda si occupa di 'Sviluppo siti web, consulenze informatiche, digitalizzazione, accessibilità, gestione server, sviluppo software, fornitura licenze software'. "
        f"Fornisci una breve spiegazione della pertinenza o indica 'Non pertinente' se non ci sono elementi rilevanti.\n"
        f"Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
        f"Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
    )
    joined_chunks = "\n\n".join([doc.page_content for doc in chunks])
    return base_prompt + "Testo:\n" + joined_chunks

def analyze_with_retrieval(text, query="bando pubblico per digitalizzazione, sviluppo software e servizi IT", k=4):
    chunks = chunk_text(text)
    vs = create_vectorstore(chunks)
    top_chunks = retrieve_top_k_chunks(vs, query=query, k=k)
    prompt = build_prompt_from_chunks(top_chunks)

    response = completion(
        messages=[{"role": "user", "content": prompt}],
        model=os.getenv("MODEL_LLM"),
        api_base=os.getenv("MODEL_LLM_API"),
        temperature=float(os.getenv("MODEL_TEMPERATURE", 0.7)),
        max_tokens=int(os.getenv("MODEL_MAX_TOKENS", 2048)),
    )

    return response["choices"][0]["message"]["content"]
