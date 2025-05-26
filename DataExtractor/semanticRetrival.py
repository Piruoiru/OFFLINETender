from pgvector_utils import connect_db

def retrieve_top_chunks(top_k=5):
    """
    Recupera i chunk semanticamente più rilevanti.

    Args:
        top_k (int): Numero massimo di chunk da restituire.

    Returns:
        list[dict]: Lista di chunk rilevanti con titolo, URL, testo e score.
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.title, d.url, c.chunk
        FROM chunks c
        JOIN documents d ON c.document_id = d.id
        LIMIT %s
    """, (top_k,))

    results = cur.fetchall()
    cur.close()
    conn.close()

    risposta = []
    for title, url, chunk, score in results:
        risposta.append({
            "Titolo": title,
            "URL": url,
            "Chunk": chunk,
        })

    return risposta

def build_prompt_from_chunks(chunks):
    """
    Descrizione: 
        Costruisce un prompt per il modello LLM unendo i chunk rilevanti.
    
    Input:
        chunks (list): Lista di oggetti Document contenenti i chunk di testo.
    
    Output:
        Stringa rappresentante il prompt.
    
    Comportamento: 
        Concatena i chunk e li aggiunge a un prompt base con istruzioni dettagliate.
    """
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
        f"- Modalità di pagamento\n"
        f"- Pertinenza con l'azienda\n\n"
        f"L'azienda si occupa di: 'Sviluppo siti web, consulenze informatiche, digitalizzazione, accessibilità, gestione server, sviluppo software, fornitura licenze software'. "
        f"Valuta quanto il contenuto è pertinente rispetto a questo ambito. Fornisci una breve spiegazione o lascia vuoto se non pertinente.\n\n"
        f"Se non trovi alcune informazioni, lascia il campo vuoto.\n\n"
        f"Rispondi solo in formato JSON valido senza ```json. Non aggiungere testo extra.\n\n"
    )
    joined_chunks = "\n\n".join([doc.page_content for doc in chunks])
    return base_prompt + "Testo:\n" + joined_chunks

def get_prompt_from_query(query_text, top_k=5):
    """
    Descrizione:
        Dato un testo di query, recupera i chunk semanticamente simili
        e costruisce un prompt per il modello LLM.

    Args:
        query_text (str): Testo della query.
        top_k (int): Numero di chunk da recuperare (default = 5).

    Returns:
        str: Prompt pronto per l'analisi da parte del modello LLM.
    """
    # 1. Recupera i chunk semanticamente simili
    retrieved_chunks_data = retrieve_top_chunks(top_k)

    # 2. Adatta i chunk in oggetti compatibili con build_prompt_from_chunks (che usa .page_content)
    class SimpleDoc:
        def __init__(self, content):
            self.page_content = content

    chunk_docs = [SimpleDoc(chunk["Chunk"]) for chunk in retrieved_chunks_data if "Chunk" in chunk]

    # 3. Costruisce il prompt
    prompt = build_prompt_from_chunks(chunk_docs)
    return prompt