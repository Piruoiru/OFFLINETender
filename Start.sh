#!/bin/bash

OLLAMA_HOST=0.0.0.0:11434 ollama serve &

echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

# Scarica i modelli richiesti
echo "Pulling required models..."
ollama pull mxbai-embed-large
ollama pull llama3.1:8b

echo "Ollama server is ready."
tail -f /dev/null