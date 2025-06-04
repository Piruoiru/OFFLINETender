from Project.Adapters.Loader.LoaderDB import LoaderDB

class DocumentRetriever:
    def __init__(self):
        self.loader = LoaderDB()
        self.documents = self.loader.documents

    def get_top_document(self, similarities):
        return similarities[0]['id'] if similarities else None

    def get_chunks_by_document_id(self, document_id):
        return self.loader.get_chunks_by_document_id(document_id)
