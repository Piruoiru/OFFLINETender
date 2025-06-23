from sklearn.metrics.pairwise import cosine_similarity

class EmbeddingSimilarityService:
    def compute_similarity(self, base_embedding, items):
        results = []
        for item in items:
            emb = item.get('embedding')
            if emb is None:
                continue
            score = cosine_similarity([base_embedding], [emb])[0][0]
            results.append({**item, 'similarity': score})
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results
