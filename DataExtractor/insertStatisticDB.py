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

        number_response_llm = get_number_response_llm_fields(document_id)

        conn = connect_db()
        cur = conn.cursor()

        query = """
        INSERT INTO statistics (
            document_id, model_llm, model_embedding, token_prompt,
            token_response, token_used, prompt, model_max_tokens,
            model_temperature, model_llm_api, model_embedding_api,
            chunk_size, chunk_overlap, number_response_llm, created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())
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
            number_response_llm,
        ))

        inserted_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return inserted_id

    except Exception as e:
        print(f"❌ Errore durante insert_statistics: {e}")
        return None


def get_number_response_llm_fields(document_id):
    try:
        conn = connect_db()
        cur = conn.cursor()

        query = """
        SELECT 
            (CASE WHEN provider IS NOT NULL AND provider <> '' THEN 1 ELSE 0 END +
             CASE WHEN publication_date IS NOT NULL AND publication_date <> '' THEN 1 ELSE 0 END +
             CASE WHEN submission_deadline IS NOT NULL AND submission_deadline <> '' THEN 1 ELSE 0 END +
             CASE WHEN procedure_title IS NOT NULL AND procedure_title <> '' THEN 1 ELSE 0 END +
             CASE WHEN purpose IS NOT NULL AND purpose <> '' THEN 1 ELSE 0 END +
             CASE WHEN funding_reference IS NOT NULL AND funding_reference <> '' THEN 1 ELSE 0 END +
             CASE WHEN cup IS NOT NULL AND cup <> '' THEN 1 ELSE 0 END +
             CASE WHEN intervention_title IS NOT NULL AND intervention_title <> '' THEN 1 ELSE 0 END +
             CASE WHEN description IS NOT NULL AND description <> '' THEN 1 ELSE 0 END +
             CASE WHEN fund IS NOT NULL AND fund <> '' THEN 1 ELSE 0 END +
             CASE WHEN required_characteristics IS NOT NULL AND required_characteristics <> '' THEN 1 ELSE 0 END +
             CASE WHEN timelines IS NOT NULL AND timelines <> '' THEN 1 ELSE 0 END +
             CASE WHEN maximum_budget IS NOT NULL AND maximum_budget <> '' THEN 1 ELSE 0 END +
             CASE WHEN deadline IS NOT NULL AND deadline <> '' THEN 1 ELSE 0 END +
             CASE WHEN email_for_quote IS NOT NULL AND email_for_quote <> '' THEN 1 ELSE 0 END +
             CASE WHEN issuer_name IS NOT NULL AND issuer_name <> '' THEN 1 ELSE 0 END +
             CASE WHEN payment_method IS NOT NULL AND payment_method <> '' THEN 1 ELSE 0 END +
             CASE WHEN company_relevance IS NOT NULL AND company_relevance <> '' THEN 1 ELSE 0 END) 
        FROM responses
        WHERE document_id = %s
        LIMIT 1;
        """

        cur.execute(query, (document_id,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        return result[0] if result else 0

    except Exception as e:
        print(f"❌ Errore durante get_number_response_llm_fields: {e}")
        return 0
