FROM python:3.11-slim

WORKDIR /App

RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    dos2unix \
    && curl -fsSL https://ollama.com/install.sh | sh \
    && apt-get clean

COPY App/ .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/App
COPY ./Start.sh /Start.sh
RUN chmod +x /Start.sh && dos2unix /Start.sh

EXPOSE 5001 11434

CMD ["/Start.sh"]