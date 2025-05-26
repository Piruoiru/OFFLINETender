import psycopg2
from pgvector.psycopg2 import register_vector
import os
from dotenv import load_dotenv

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

def insert_chunks(chunks, embeddings, document_id):
    """
    Inserisce una lista di chunk e embedding associati nella tabella `chunks`.
    """
    conn = connect_db()
    cur = conn.cursor()
    chunk_ids = []

    for chunk, embedding in zip(chunks, embeddings):
        if embedding is None:
            continue  # Skip if embedding is None

        # ✅ Rimuovi caratteri null dal chunk
        clean_chunk = chunk.replace('\x00', '')

        cur.execute("""
        INSERT INTO chunks (chunk, embedding, document_id)
        VALUES (%s, %s, %s)
        RETURNING id
        """, (clean_chunk, embedding, document_id))
        chunk_ids.append(cur.fetchone()[0])

    
    conn.commit()
    cur.close()
    conn.close()
    return chunk_ids

def insert_document(title, url, hash, site_id):
    """
    Inserisce ogni titolo e url nella tabella `documents`.
    """
    conn = connect_db()
    cur = conn.cursor()
    document_id = None

    cur.execute("""
        INSERT INTO documents (title, url, hash, site_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (title, url, hash, site_id))

    document_id = cur.fetchone()[0]  

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


# def normalize_llm_response(raw_response):
#     """
#     Converte i nomi dei campi da linguaggio naturale a snake_case per il DB.
#     """
#     mapping = {
#         "Provider": "provider",
#         "Data di pubblicazione": "data_di_pubblicazione",
#         "Data di termine di consegna": "data_di_termine_consegna",
#         "Tipologia di procedura": "titolo_procedura",
#         "Finalità": "finalita",
#         "Riferimento finanziamento": "riferimento_finanziamento",
#         "CUP": "cup",
#         "Titolo dell'intervento": "titolo_dell_intervento",
#         "Descrizione": "descrizione",
#         "Fondo": "fondo",
#         "Caratteristiche richieste": "caratteristiche_richieste",
#         "Tempistiche": "tempistiche",
#         "Budget massimo": "budget_massimo",
#         "Deadline": "deadline",
#         "Mail a cui mandare la quota": "mail_a_cui_mandare_la_quota",
#         "Nome emittente": "nome_emittente",
#         "Modalità di pagamento": "modalita_di_pagamento",
#         "Pertinenza con l'azienda": "pertinenza_con_lazienda"
#     }

#     normalized = {}
#     for old_key, new_key in mapping.items():
#         normalized[new_key] = raw_response.get(old_key, None)

#     return normalized

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

# def document_is_fully_processed(doc_hash):
#     """
#     Verifica se il documento ha sia chunk che risposta.
#     """
#     conn = connect_db()
#     cur = conn.cursor()
#     cur.execute("""
#         SELECT EXISTS (
#             SELECT 1
#             FROM documents d
#             JOIN responses r ON r.document_id = d.id
#             JOIN chunks c ON c.document_id = d.id
#             WHERE d.hash = %s
#         )
#     """, (doc_hash,))
#     result = cur.fetchone()[0]
#     cur.close()
#     conn.close()
#     return result

#     return result is not None

def get_document_id_by_hash(doc_hash):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM documents WHERE hash = %s", (doc_hash,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[0] if result else None

def document_has_chunks(doc_id):
    """
    Controlla se esistono chunk per il documento.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM chunks WHERE document_id = %s LIMIT 1", (doc_id,))
    result = cur.fetchone() is not None
    cur.close()
    conn.close()
    return result

def document_has_response(doc_id):
    """
    Controlla se esiste una risposta per il documento.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM responses WHERE document_id = %s LIMIT 1", (doc_id,))
    result = cur.fetchone() is not None
    cur.close()
    conn.close()
    return result