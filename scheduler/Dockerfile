FROM python:3.10-slim

WORKDIR /app
COPY app/ ./app/

RUN pip install fastapi uvicorn pika sqlalchemy psycopg2-binary requests

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
