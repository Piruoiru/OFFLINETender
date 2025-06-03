import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from project.use_cases.ContextExtractor import ContextExtractor
from project.adapters.LLM.LLMResponceService import LLMResponseService

class QueryProcessor:
    def __init__(self):
        self.context_extractor = ContextExtractor()
        self.llm_service = LLMResponseService()

    def run(self, user_input: str):
        # Step 1: Estrai contesto rilevante
        try:
            top_chunks = self.context_extractor.process_user_input(user_input)
        except Exception as e:
            return {"error": f"Errore nel recupero del contesto: {str(e)}"}

        # Step 2: Costruisci il prompt
        context_text = "\n\n".join([c['chunk'] for c in top_chunks])
        prompt = (
            f"Contesto:\n{context_text}\n\n"
            f"Domanda:\n{user_input}\n\n"
            f"Rispondi usando solo le informazioni nel contesto."
        )

        # Step 3: Ottieni risposta dal modello LLM
        try:
            response = self.llm_service.get_LLM_response(prompt)
            return response
        except Exception as e:
            return {"error": f"Errore dal modello LLM: {str(e)}"}


if __name__ == "__main__":
    qp = QueryProcessor()
    user_query = input("Inserisci la tua domanda: ").strip()
    result = qp.run(user_query)
    print("\nRisposta:\n", result)