from DataExtractor.embedderLocal import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import CrossEncoder
from LoaderDB import LoaderDB  # ✅ aggiunto import

TOP_CHUNKS = 10
FINAL_TOP = 3
CROSS_ENCODER_MODEL = 'cross-encoder/ms-marco-electra-base'

class ContextExtractor:
    def __init__(self):
        self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
        self.loader = LoaderDB()  # ✅ istanzia LoaderDB
        self.documents = self.loader.documents  # ✅ carica documenti una volta sola

    def process_user_input(self, user_input: str):
        user_embedding = get_embedding(user_input)
        if user_embedding is None:
            raise ValueError("❌ Embedding non calcolato.")

        # 🔹 Similarità tra input utente e documenti
        similarities = []
        for doc in self.documents:
            emb = doc.get('embedding')
            if emb is None:
                continue
            score = cosine_similarity([user_embedding], [emb])[0][0]
            similarities.append({**doc, 'similarity': score})

        similarities.sort(key=lambda x: x['similarity'], reverse=True)
        top_doc_id = similarities[0]['id']

        # 🔹 Recupero chunk tramite LoaderDB
        chunk_rows = self.loader.get_chunks_by_document_id(top_doc_id)  # ✅ usa metodo da LoaderDB

        candidate_chunks = []
        for row in chunk_rows:
            emb = row['embedding']
            if emb is None:
                continue
            score = cosine_similarity([user_embedding], [emb])[0][0]
            candidate_chunks.append({
                'id': row['id'],
                'chunk': row['chunk'],
                'embedding': emb,
                'similarity': score
            })

        # 🔹 Top chunk con bi-encoder
        candidate_chunks.sort(key=lambda x: x['similarity'], reverse=True)
        top_candidates = candidate_chunks[:TOP_CHUNKS]

        # 🔹 Reranking con cross-encoder
        inputs = [[user_input, c['chunk']] for c in top_candidates]
        scores = self.cross_encoder.predict(inputs)
        for idx, score in enumerate(scores):
            top_candidates[idx]['rerank_score'] = score

        top_candidates.sort(key=lambda x: x['rerank_score'], reverse=True)
        return top_candidates[:FINAL_TOP]
