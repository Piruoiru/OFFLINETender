from sentence_transformers import CrossEncoder
from Project.Core.Services.EmbedderLocal import get_embedding
from Project.Core.Services.EmbeddingSimilarityService import EmbeddingSimilarityService
from Project.Adapters.Database.DocumentRetriver import DocumentRetriever


TOP_CHUNKS = 10
FINAL_TOP = 3
CROSS_ENCODER_MODEL = 'cross-encoder/ms-marco-electra-base'

class ContextExtractor:
    def __init__(self):
        self.cross_encoder = CrossEncoder(CROSS_ENCODER_MODEL)
        self.retriever = DocumentRetriever()
        self.similarity_service = EmbeddingSimilarityService()

    def process_user_input(self, user_input: str):
        user_embedding = get_embedding(user_input)
        if user_embedding is None:
            raise ValueError("❌ Embedding non calcolato.")

        doc_similarities = self.similarity_service.compute_similarity(user_embedding, self.retriever.documents)
        top_doc_id = self.retriever.get_top_document(doc_similarities)
        chunk_rows = self.retriever.get_chunks_by_document_id(top_doc_id)

        top_chunks = self.similarity_service.compute_similarity(user_embedding, chunk_rows)[:TOP_CHUNKS]

        reranked_chunks = sorted(
            top_chunks,
            key=lambda x: self.cross_encoder.predict([(user_input, x['chunk'])])[0],
            reverse=True
        )[:FINAL_TOP]

        return reranked_chunks
