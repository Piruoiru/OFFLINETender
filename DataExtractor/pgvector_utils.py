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

def insert_pdf_link_to_site_table(url, title=None):
    """
    Inserisce un link PDF nella tabella `site` se non esiste già.
    Salva anche il titolo del link, se fornito.

    Args:
        url (str): URL del PDF da registrare.
        title (str): Titolo o testo del link (opzionale).

    Returns:
        int: ID del sito registrato o già presente.
    """
    conn = connect_db()
    cur = conn.cursor()

    # Verifica se già esiste
    cur.execute("SELECT idsite FROM site WHERE sitetoscrape = %s", (url,))
    result = cur.fetchone()

    if result:
        site_id = result[0]
        # Se già presente ma vogliamo aggiornare il titolo (opzionale)
        if title:
            cur.execute("UPDATE site SET title = %s WHERE idsite = %s", (title, site_id))
            conn.commit()
    else:
        cur.execute("INSERT INTO site (sitetoscrape, title) VALUES (%s, %s) RETURNING idsite", (url, title))
        site_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return site_id

def insert_chunk(title, url, chunk, embedding, site_id=None, chunk_id=None, risposta_id=None):
    """
    Inserisce un chunk con embedding nella tabella DocumentChunk.

    Args:
        title (str): Titolo del documento.
        url (str): URL sorgente.
        chunk (str): Contenuto del chunk.
        embedding (list): Vettore embedding.
        site_id (int, optional): ID del sito di origine.
        chunk_id (str, optional): Identificativo logico del chunk.
        risposta_id (int, optional): ID della risposta LLM associata.

    Returns:
        None
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO DocumentChunk (title, url, site_id, chunk_id, chunk, embedding, risposta_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (title, url, site_id, chunk_id, chunk, embedding, risposta_id))

    conn.commit()
    cur.close()
    conn.close()

def insert_response(response_data):
    """
    Inserisce una risposta LLM nel DB e ritorna l'ID.

    Args:
        response_data (dict): Risposta JSON già validata.

    Returns:
        int: ID della riga inserita.
    """
    conn = connect_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO Response (
            provider, data_di_pubblicazione, data_di_termine_consegna,
            titolo_procedura, finalita, riferimento_finanziamento,
            cup, titolo_dell_intervento, descrizione, fondo,
            caratteristiche_richieste, tempistiche, budget_massimo,
            deadline, mail_a_cui_mandare_la_quota, nome_emittente,
            modalita_di_pagamento, pertinenza_con_lazienda
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (
        response_data.get("provider"),
        response_data.get("data_di_pubblicazione"),
        response_data.get("data_di_termine_consegna"),
        response_data.get("titolo_procedura"),
        response_data.get("finalita"),
        response_data.get("riferimento_finanziamento"),
        response_data.get("cup"),
        response_data.get("titolo_dell_intervento"),
        response_data.get("descrizione"),
        response_data.get("fondo"),
        response_data.get("caratteristiche_richieste"),
        response_data.get("tempistiche"),
        response_data.get("budget_massimo"),
        response_data.get("deadline"),
        response_data.get("mail_a_cui_mandare_la_quota"),
        response_data.get("nome_emittente"),
        response_data.get("modalita_di_pagamento"),
        response_data.get("pertinenza_con_lazienda")
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