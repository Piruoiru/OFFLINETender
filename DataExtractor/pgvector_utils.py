import psycopg2
from pgvector.psycopg2 import register_vector
import os
from dotenv import load_dotenv
from chunkizer import chunk_text
from embedderLocal import get_embeddings_parallel
import PyPDF2
from io import BytesIO
import hashlib


load_dotenv()

def connect_db():
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", 5433)
    )
    register_vector(conn)
    return conn

def insert_sites(site_url):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("SELECT id FROM sites WHERE site_to_scrape = %s", (site_url,))
    result = cur.fetchone()

    if result:
        site_id = result[0]
    else:
        cur.execute("INSERT INTO sites (site_to_scrape) VALUES (%s) RETURNING id", (site_url,))
        site_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return site_id

def insert_documents(title, url, chunk, embedding, site_id=None):
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents (title, url, chunk, site_id, embedding)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (title, url, chunk, site_id, embedding))

    conn.commit()
    cur.close()
    conn.close()

def insert_document_chunks(title, url, chunks, embeddings, site_id):
    """
    Inserisce ogni chunk nella tabella `documents`.
    Ritorna l'id del primo chunk inserito (come rappresentante del documento).
    """
    conn = connect_db()
    cur = conn.cursor()
    document_id = None

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        if embedding is None:
            continue
        cur.execute("""
            INSERT INTO documents (title, url, chunk, embedding, site_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (title, url, chunk, embedding, site_id))
        
        # Prendi l'id solo del primo chunk inserito
        if document_id is None:
            document_id = cur.fetchone()[0]
        else:
            cur.fetchone()  # consumare comunque il risultato per gli altri

    conn.commit()
    cur.close()
    conn.close()
    return document_id

def insert_response(response_data, document_id=None):
    """
    Inserisce una risposta LLM nella tabella `responses` e ritorna l'ID.

    Args:
        response_data (dict): Risposta JSON già validata.

    Returns:
        int: ID della riga inserita.
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO responses (
        provider, publication_date, submission_deadline,
        procedure_title, purpose, funding_reference,
        cup, intervention_title, description, fund,
        required_characteristics, timelines, maximum_budget,
        deadline, email_for_quote, issuer_name,
        payment_method, company_relevance, document_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """, (
        response_data.get("provider"),
        response_data.get("publication_date"),
        response_data.get("submission_deadline"),
        response_data.get("procedure_title"),
        response_data.get("purpose"),
        response_data.get("funding_reference"),
        response_data.get("cup"),
        response_data.get("intervention_title"),
        response_data.get("description"),
        response_data.get("fund"),
        response_data.get("required_characteristics"),
        response_data.get("timelines"),
        response_data.get("maximum_budget"),
        response_data.get("deadline"),
        response_data.get("email_for_quote"),
        response_data.get("issuer_name"),
        response_data.get("payment_method"),
        response_data.get("company_relevance"),
        document_id
    ))

    response_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return response_id


def normalize_llm_response(raw_response):
    """
    Converte i nomi dei campi da linguaggio naturale a snake_case per il DB.
    """
    mapping = {
        "Provider": "provider",
        "Data di pubblicazione": "data_di_pubblicazione",
        "Data di termine di consegna": "data_di_termine_consegna",
        "Tipologia di procedura": "titolo_procedura",
        "Finalità": "finalita",
        "Riferimento finanziamento": "riferimento_finanziamento",
        "CUP": "cup",
        "Titolo dell'intervento": "titolo_dell_intervento",
        "Descrizione": "descrizione",
        "Fondo": "fondo",
        "Caratteristiche richieste": "caratteristiche_richieste",
        "Tempistiche": "tempistiche",
        "Budget massimo": "budget_massimo",
        "Deadline": "deadline",
        "Mail a cui mandare la quota": "mail_a_cui_mandare_la_quota",
        "Nome emittente": "nome_emittente",
        "Modalità di pagamento": "modalita_di_pagamento",
        "Pertinenza con l'azienda": "pertinenza_con_lazienda"
    }

    normalized = {}
    for old_key, new_key in mapping.items():
        normalized[new_key] = raw_response.get(old_key, None)

    return normalized

def retrieve_top_chunks_from_document(embeddings, chunks, top_k=5):
    """
    Ordina i chunk locali in base alla distanza coseno interna.
    """
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity

    if not embeddings or len(embeddings) < top_k:
        return chunks

    sims = cosine_similarity(embeddings, embeddings)
    avg_scores = sims.mean(axis=1)
    top_indices = np.argsort(avg_scores)[-top_k:][::-1]

    top_chunks = [chunks[i] for i in top_indices]
    return top_chunks