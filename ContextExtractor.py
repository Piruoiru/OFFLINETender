# from DataExtractor.pgvector_utils import connect_db
# from DataExtractor.embedderLocal import get_embedding
# import psycopg2.extras
# from sklearn.metrics.pairwise import cosine_similarity
# from sentence_transformers import CrossEncoder

# TOP_CHUNKS = 10
# FINAL_TOP = 3
# CROSS_ENCODER_MODEL = 'cross-encoder/ms-marco-MiniLM-L-6-v2'

# class ContextExtractor:
#     def __init__(self):
#         self.dbConnection = connect_db()
#         self.documents = self.load_documents()
#         self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

#     def process_user_input(self, user_input: str):
#         user_embedding = get_embedding(user_input)
#         if user_embedding is None:
#             raise ValueError("❌ Embedding non calcolato.")

#         # 🔹 Similarità tra input utente e documenti
#         similarities = []
#         for doc in self.documents:
#             emb = doc.get('embedding')
#             if emb is None:
#                 continue
#             score = cosine_similarity([user_embedding], [emb])[0][0]
#             similarities.append({**doc, 'similarity': score})

#         similarities.sort(key=lambda x: x['similarity'], reverse=True)
#         top_doc_id = similarities[0]['id']

#         # 🔹 Recupera chunk solo del documento più simile
#         with self.dbConnection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#             cursor.execute("SELECT id, chunk, embedding FROM chunks WHERE document_id = %s", (top_doc_id,))
#             chunk_rows = cursor.fetchall()

#         candidate_chunks = []
#         for row in chunk_rows:
#             emb = row['embedding']
#             if emb is None:
#                 continue
#             score = cosine_similarity([user_embedding], [emb])[0][0]
#             candidate_chunks.append({
#                 'id': row['id'],
#                 'chunk': row['chunk'],
#                 'embedding': emb,
#                 'similarity': score
#             })

#         # 🔹 Top chunk con bi-encoder
#         candidate_chunks.sort(key=lambda x: x['similarity'], reverse=True)
#         top_candidates = candidate_chunks[:TOP_CHUNKS]

#         # 🔹 Reranking con cross-encoder
#         inputs = [[user_input, c['chunk']] for c in top_candidates]
#         scores = self.cross_encoder.predict(inputs)
#         for idx, score in enumerate(scores):
#             top_candidates[idx]['rerank_score'] = score

#         top_candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
#         return top_candidates[:FINAL_TOP]

#     def load_documents(self):
#         """
#         Carica tutti i documenti dal DB con il loro embedding.
#         """
#         with self.dbConnection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#             cursor.execute("SELECT id, title, url, document_embedding FROM documents WHERE document_embedding IS NOT NULL")
#             rows = cursor.fetchall()

#         documents = []
#         for row in rows:
#             documents.append({
#                 'id': row['id'],
#                 'title': row['title'],
#                 'url': row['url'],
#                 'embedding': row['document_embedding']
#             })
#         return documents

#     def __del__(self):
#         if hasattr(self, 'dbConnection'):
#             self.dbConnection.close()


# if __name__ == "__main__":
#     print("🔍 Avvio del ContextExtractor...\n")
#     extractor = ContextExtractor()

#     user_input = input("Inserisci una domanda o testo da cercare: ").strip()

#     if not user_input:
#         print("❌ Nessun input fornito.")

#     print("\n🔎 Elaborazione della query...")
#     top_chunks = extractor.process_user_input(user_input)

#     print(f"\n✅ Top {len(top_chunks)} chunk più rilevanti:\n")
#     for i, chunk in enumerate(top_chunks, start=1):
#         print(f"--- Chunk #{i} (Score: {chunk.get('rerank_score'):.4f}) ---")
#         print(chunk['chunk'])
#         print()
from DataExtractor.pgvector_utils import connect_db
from DataExtractor.embedderLocal import get_embedding
import psycopg2.extras
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import CrossEncoder

TOP_DOCS = 3
TOP_CHUNKS = 10
FINAL_TOP = 3
CROSS_ENCODER_MODEL = 'cross-encoder/ms-marco-MiniLM-L-6-v2'


class ContextExtractor:
    def __init__(self):
        self.dbConnection = connect_db()
        self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)

    def process_user_input(self, user_input: str):
        user_embedding = get_embedding(user_input)
        if user_embedding is None:
            raise ValueError("❌ Embedding non calcolato.")

        # 🔹 Carica documenti filtrati per contenuto testuale
        documents = self.load_documents(user_input)

        if not documents:
            print("⚠️ Nessun documento filtrato testualmente. Fallback a tutti i documenti...")
            documents = self.load_documents()

        # 🔹 Similarità tra input utente e documenti
        similarities = []
        for doc in documents:
            emb = doc.get('embedding')
            if emb is None:
                continue
            score = cosine_similarity([user_embedding], [emb])[0][0]
            similarities.append({**doc, 'similarity': score})

        if not similarities:
            print("❌ Nessun documento con embedding valido trovato.")
            return []

        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_doc_ids = [doc['id'] for doc in similarities[:TOP_DOCS]]

        # 🔹 Recupera i chunk dai top documenti
        candidate_chunks = []
        with self.dbConnection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute(
                "SELECT id, document_id, chunk, embedding FROM chunks WHERE document_id = ANY(%s)",
                (top_doc_ids,)
            )
            chunk_rows = cursor.fetchall()

        for row in chunk_rows:
            emb = row['embedding']
            if emb is None:
                continue
            score = cosine_similarity([user_embedding], [emb])[0][0]
            candidate_chunks.append({
                'id': row['id'],
                'document_id': row['document_id'],
                'chunk': row['chunk'],
                'embedding': emb,
                'similarity': score
            })

        if not candidate_chunks:
            print("❌ Nessun chunk valido trovato.")
            return []

        # 🔹 Bi-encoder filtering
        candidate_chunks.sort(key=lambda x: x['similarity'], reverse=True)
        top_candidates = candidate_chunks[:TOP_CHUNKS]

        # 🔹 Reranking con CrossEncoder
        inputs = [[user_input, c['chunk']] for c in top_candidates]
        scores = self.cross_encoder.predict(inputs)
        for idx, score in enumerate(scores):
            top_candidates[idx]['rerank_score'] = score

        top_candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        return top_candidates[:FINAL_TOP]

    def load_documents(self, user_input: str = None):
        """
        Carica documenti dal DB. Se fornito user_input, applica filtro testuale.
        """
        with self.dbConnection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            if user_input:
                cursor.execute("""
                    SELECT id, title, url, document_embedding
                    FROM documents
                    WHERE content ILIKE %s AND document_embedding IS NOT NULL
                """, (f"%{user_input}%",))
            else:
                cursor.execute("""
                    SELECT id, title, url, document_embedding
                    FROM documents
                    WHERE document_embedding IS NOT NULL
                """)
            rows = cursor.fetchall()

        return [{
            'id': row['id'],
            'title': row['title'],
            'url': row['url'],
            'embedding': row['document_embedding']
        } for row in rows]

    def __del__(self):
        if hasattr(self, 'dbConnection'):
            self.dbConnection.close()


if __name__ == "__main__":
    print("🔍 Avvio del ContextExtractor...\n")
    extractor = ContextExtractor()

    user_input = input("Inserisci una domanda o testo da cercare: ").strip()

    if not user_input:
        print("❌ Nessun input fornito.")

    print("\n🔎 Elaborazione della query...")
    top_chunks = extractor.process_user_input(user_input)

    print(f"\n✅ Top {len(top_chunks)} chunk più rilevanti:\n")
    for i, chunk in enumerate(top_chunks, start=1):
        print(f"--- Chunk #{i} (Score: {chunk.get('rerank_score'):.4f}) ---")
        print(chunk['chunk'])
        print()
