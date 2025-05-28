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
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )
    register_vector(conn)
    return conn

def insert_statistics(document_id, token_prompt, token_response, prompt):
    try:
        token_used = token_prompt + token_response

        # Parametri da .env
        model_llm = os.getenv("MODEL_LLM")
        model_embedding = os.getenv("MODEL_EMBEDDING")
        model_llm_api = os.getenv("MODEL_LLM_API")
        model_embedding_api = os.getenv("MODEL_EMBEDDING_API")
        model_max_tokens = int(os.getenv("MODEL_MAX_TOKENS"))
        model_temperature = float(os.getenv("MODEL_TEMPERATURE"))
        chunk_size = int(os.getenv("CHUNK_SIZE"))
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP"))

        conn = connect_db()
        cur = conn.cursor()

        query = """
        INSERT INTO statistics (
            document_id, model_llm, model_embedding, token_prompt,
            token_response, token_used, prompt, model_max_tokens,
            model_temperature, model_llm_api, model_embedding_api,
            chunk_size, chunk_overlap, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())
        RETURNING id
        """

        cur.execute(query, (
            document_id,
            model_llm,
            model_embedding,
            token_prompt,
            token_response,
            token_used,
            prompt,
            model_max_tokens,
            model_temperature,
            model_llm_api,
            model_embedding_api,
            chunk_size,
            chunk_overlap,
        ))

        inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return inserted_id

    except Exception as e:
        print(f"❌ Errore durante insert_statistics: {e}")
        return None
