FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY vectordb ./vectordb

ENV OPENAI_MODEL=gpt-4o-mini
ENV CHROMA_DB_DIR=vectordb
ENV COLLECTION_NAME=normas_auditoria

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
