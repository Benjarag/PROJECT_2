FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r --no-cache-dir requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", ", --port", "8001"]

