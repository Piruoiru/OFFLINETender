import sys
import json
from QueryProcessor import QueryProcessor

def main():
    user_input = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else None
    if not user_input:
        print(json.dumps({'error': 'Messaggio utente mancante'}))
        sys.exit(1)

    user_input = sys.argv[1]
    conversation_id = sys.argv[2] if len(sys.argv) > 2 else None

    qp = QueryProcessor(conversation_id)
    result = qp.run(user_input)

    # Se è un dict (errore), stampalo come JSON
    if isinstance(result, dict):
        print(json.dumps(result))
    else:
        print(json.dumps({
            'response': result,
            'conversation_id': qp.conversation_id
        }))

if __name__ == '__main__':
    main()
