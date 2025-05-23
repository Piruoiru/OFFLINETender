FROM python:3.11-slim

# Crea directory dell'app
WORKDIR /app

# Copia i file
COPY . /app

RUN pip install --upgrade pip

# Installa le dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta Flask
EXPOSE 5000

# Comando per avviare l'app Flask
CMD ["python", "analyzer.py"]