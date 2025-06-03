from project.adapters.database.pgvector_utils import connect_db
import psycopg2.extras

class LoaderDB:
    def __init__(self):
        self.dbConnection = connect_db()
        self.documents = self.load_documents()

    def load_documents(self):
        """
        Carica tutti i documenti dal DB con il loro embedding.
        """
        with self.dbConnection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("SELECT id, title, url, document_embedding FROM documents WHERE document_embedding IS NOT NULL")
            rows = cursor.fetchall()

        documents = []
        for row in rows:
            documents.append({
                'id': row['id'],
                'title': row['title'],
                'url': row['url'],
                'embedding': row['document_embedding']
            })
        return documents
    
    def get_chunks_by_document_id(self, document_id):
        """
        Recupera tutti i chunk e i relativi embedding per un dato documento.
        """
        conn = connect_db()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT id, chunk, embedding FROM chunks WHERE document_id = %s", (document_id,))
        rows = cur.fetchall()

        cur.close()
        conn.close()
        return rows

    def __del__(self):
        if hasattr(self, 'dbConnection'):   
            self.dbConnection.close()
