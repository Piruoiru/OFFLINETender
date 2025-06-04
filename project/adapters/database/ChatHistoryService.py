import psycopg2
import os

class ChatHistoryService:
    def __init__(self):
        self.conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT")
    )

    def create_conversation(self) -> int:
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO conversations (active) VALUES (TRUE) RETURNING id")
            conversation_id = cur.fetchone()[0]
            self.conn.commit()
            return conversation_id

    def save_message(self, conversation_id: int, sender: str, content: str):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (conversation_id, sender, content)
                VALUES (%s, %s, %s)
            """, (conversation_id, sender, content))
            self.conn.commit()

    def get_history(self, conversation_id: int, limit: int = 10):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT sender, content FROM messages
                WHERE conversation_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """, (conversation_id, limit))
            return cur.fetchall()
