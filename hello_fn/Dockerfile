FROM python:3.10-slim

WORKDIR /app
COPY handler.py .
COPY runner.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "runner.py"]

