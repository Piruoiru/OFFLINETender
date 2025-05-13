#!/bin/bash

OLLAMA_HOST=0.0.0.0:11434 ollama serve &

echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

# scarica il modello di embedding e il LLM
echo "Pulling required models..."
ollama pull mxbai-embed-large
ollama run llama3.1:8b

until pg_isready -h db -p 5432 -U postgres; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done


# Avvia l'applicazione Flask con Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 --timeout 1000 Main:flaskApp